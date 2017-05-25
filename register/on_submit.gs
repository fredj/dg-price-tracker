var authHeader = {
  'Authorization': 'token CHANGE_ME'
};
var productsUrl = 'https://api.github.com/repos/fredj/dg-price-tracker/contents/products.csv?ref=gh-pages'
var issueUrl = 'https://api.github.com/repos/fredj/dg-price-tracker/issues'

function onFormSubmit(event) {
  // get products.csv
  var entry = UrlFetchApp.fetch(productsUrl, {
    'headers': authHeader
  });
  entry = JSON.parse(entry.getContentText());

  var content = UrlFetchApp.fetch(entry['download_url'], {
    'headers': authHeader
  });
  content = content.getContentText();

  // compute product id
  var product_id = productId(event.values[1]);
  if (product_id) {
    content = content + '\n' + product_id + ',,,';

    // FIXME: check if product already tracked

    var title = 'from docs.google.com/spreadsheet';
    var body = content;

    var commit = {
      'message': 'New product from google form',
      'content': Utilities.base64Encode(content),
      'sha': entry['sha'],
      'branch': 'gh-pages'
    };

    var options = {
      'method': 'PUT',
      'headers': authHeader,
      'contentType': "application/json",
      'payload': JSON.stringify(commit)
    };
    var response = UrlFetchApp.fetch(productsUrl, options);
  }
}

function productId(url) {
  // FIXME: validate host
  // FIXME: validate is a product
  var match = url.match(/.*-(\d*)/);
  if (match) {
    var id;
    if (url.indexOf('https://www.galaxus.ch') == 0) {
      id = 'g.'
    } else if (url.indexOf('https://www.digitec.ch') == 0) {
      id = 'd.'
    }
    id += match[1];
    return id;
  } else {
    Logger.log('Invalid url: %s', url)
  }
}
