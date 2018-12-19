const path = require('path');
const merge = require('webpack-merge');
const CleanWebpackPlugin = require('clean-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin');

const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'production',
  output: {
    path: path.join(__dirname, 'build')
  },
  plugins: [
    new CleanWebpackPlugin(['build']),
    new CopyWebpackPlugin([
      { from: 'assets' }
    ])
  ]
});