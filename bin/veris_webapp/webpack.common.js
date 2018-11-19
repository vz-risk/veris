const path = require('path')
const webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const ExtractTextPlugin = require('extract-text-webpack-plugin')

module.exports = {
  entry: [
    './src/js/main.js',
    './assets/css/dbir.css'
  ],
  output: {
    path: path.join(__dirname, 'dist', 'dbir-web'),
    filename: 'js/main.min.js',
    publicPath: ''
  },
  plugins: [
    new ExtractTextPlugin("styles.css"),
    new HtmlWebpackPlugin({
      title: 'VERIS Webapp',
      template: path.join(__dirname, 'assets', 'index.html'),
      inlineSource: '.(js|css)$'
    })
  ],
  devtool: 'inline-source-map',
  devServer: {
    contentBase: 'assets'
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
        loader: 'babel-loader',
        query: {
          presets: ['env', 'react', 'stage-2'],
          plugins: ['transform-decorators-legacy', 'inline-json-import']
        }
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract({
          fallback: "style-loader",
          use: "css-loader"
        })
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx', '.css'],
    modules: [
      'node_modules'
    ]        
  }
}
