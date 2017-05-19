const autobind = document.querySelector('dom-bind');

d3.csv('products.csv', (products) => {
  autobind.products = products
});
