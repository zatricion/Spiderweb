//
// Visualization
//

var getFavicon = function (url, callback) {
  var favicon;
  // Parse url
  var a = document.createElement('a');
  a.href = url;
  var domain = 'http://' + a.hostname;
  var oneSlash = /^(\/)(?!\/)/;
  var dfd = $.Deferred();

  var _getFavicon = function (favCache) {
    favCache = favCache || {};
    if (favCache[url]) {
      favicon = favCache[url];
      callback(url, favicon);
      dfd.resolve();
    } else {
      $.get(url)
          .success(
            function (data) {
              favicon =  $("<div>").html(data)
                                   .find('link[rel="icon"], link[rel="shortcut icon"]')
                                   .attr("href");
              if (favicon) {
                // See if the favicon needs the domain prepended
                if (!/^(https?:)?\/{2}/.test(favicon)) {
                  if (oneSlash.test(favicon)) {
                    favicon = domain + favicon;
                  } else {
                    favicon = domain + '/' + favicon;
                  }
                }
              } else {
                  favicon = domain + '/favicon.ico';
              }

              // Cache favicon
              favCache[url] = favicon;
              localStorage.setItem("favicons", JSON.stringify(favCache));

              callback(url, favicon);
              dfd.resolve();
              })
        .error(
            function () {
              favicon = domain + '/favicon.ico';

              // Cache favicon
              favCache[url] = favicon;
              localStorage.setItem("favicons", JSON.stringify(favCache));

              callback(url, favicon);
              dfd.resolve();
            });
    }
  }

  // Try to get favicon from cache, otherwise find it, then cache it
  var favicon_cache = JSON.parse(localStorage.getItem("favicons"));
  _getFavicon(favicon_cache);

  return dfd.promise();
}

var getPathmark = function (pathmarks, links) {
    pathmarks.forEach(function (mark) {
            var link = {
              source: mark[0],
              target: mark[1],
            };

            links.push(link);
        });

  console.log(pathmarks);
  getNodes(links);
}

var onWindowResize = function (event) {
  overlayContext.clearRect( 0, 0, overlay.width, overlay.height );
  width = window.innerWidth;
  height = window.innerHeight;
  overlay.width = width;
  overlay.height = height;
  overlayContext.fillStyle = 'rgba( 0, 0, 0, 1 )';
  overlayContext.fillRect( 0, 0, overlay.width, overlay.height );
}

var clearScreen = function () {
  d3.select('svg').remove();
  d3.select('canvas').remove();
  d3.select('#tooltip').remove();
  document.removeEventListener('keydown', keyListener, false);
}

var visualize = function (pathmark) {
  overlay = document.createElement( 'canvas' );
  var html = document.getElementsByTagName("html")[0];
  html.appendChild(overlay);
  overlayContext = overlay.getContext( '2d' );
  overlay.style.position = 'fixed';
  overlay.style.left = 0;
  overlay.style.top = 0;
  overlay.style.zIndex = 111111111;
  onWindowResize();

  // Remove Visualization on background click
  overlay.addEventListener('click', clearScreen, false);

  // Resize canvas when window is resized
  window.addEventListener('resize', onWindowResize, false);

  // Tab and Esc key listener
  document.addEventListener('keydown', keyListener, false);

  getPathmark(pathmark, []);
}

// Compute the distinct nodes from the links.
var getNodes = function (links) {
  var width = window.innerWidth;
  var height = window.innerHeight;

  var nodes = {};
  links.forEach(function(link) {
    link.target = nodes[link.target] ||
      (nodes[link.target] = {
         name: link.target,
           xt: width / 2,
            y: height / 2,
      });
  });

  links.forEach(function(link) {
    link.source = nodes[link.source] ||
      (nodes[link.source] = {
         name: link.source,
           xt: width / 2,
            y: height / 2,
      });
  });

  urlArr = Object.keys(nodes);

  var deferred = [];
  for (var i = 0; i < urlArr.length; i++) {
    // Get all favicons before drawing visualization
    deferred.push(
        getFavicon(urlArr[i], function (url, favicon) {
          nodes[url].favicon = favicon;}));
  }
  $.when.apply($, deferred).then(function () {
    // Call D3 script
    plotPathmark(links, nodes, width, height);
  });
}


// Esc key clears the screen, tab switches visualization
var keyListener = function(e) {
  if (e.keyCode === 27) {
    clearScreen();
  } else if (e.keyCode === 9) {
    e.preventDefault();
    switchVis();
  }
}

