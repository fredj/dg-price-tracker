const margin = {top: 20, right: 20, bottom: 30, left: 50};
const width = 700 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

const x = d3.scaleTime().range([0, width]);
const y = d3.scaleLinear().range([height, 0]);

const xaxis = d3.axisBottom(x).ticks(d3.timeDay);
const yaxis = d3.axisLeft(y);

const svg = d3.select('#graph').append('svg')
  .attr('width', width + margin.left + margin.right)
  .attr('height', height + margin.top + margin.bottom)
  .append('g')
  .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

const line = d3.line()
  .x(function(d) { return x(d.date); })
  .y(function(d) { return y(d.price); });


const parseDate = d3.timeParse('%Y-%m-%d');

d3.csv('prices/d.295351.csv', (prices) => {
  prices.forEach((price) => {
    price.date = parseDate(price.date);
    price.price = parseFloat(price.price);
  });

  x.domain([
    d3.min(prices, price => price.date),
    d3.max(prices, price => price.date)
  ]);
  y.domain([0, d3.max(prices, price => price.price)]);

  // x axis
  svg.append('g')
    .attr('transform', 'translate(0,' + height + ')')
    .call(xaxis);

  // y axis
  svg.append('g')
    .call(yaxis);

  // line
  svg.append('path')
    .attr('class', 'line')
    .attr('d', line(prices));
});
