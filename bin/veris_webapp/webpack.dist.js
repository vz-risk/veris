const path = require('path');
//const merge = require('webpack-merge');
const { merge } = require('webpack-merge');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const HtmlWebpackInlineSourcePlugin = require('html-webpack-inline-source-plugin');

const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'production',
  plugins: [
    new HtmlWebpackPlugin({
      title: 'VERIS Webapp',
      template: path.join(__dirname, 'assets', 'index.html'),
      inlineSource: '.(js|css)$',
      filename: 'index.html'
    }),
    new HtmlWebpackInlineSourcePlugin(HtmlWebpackPlugin)
  ]
});