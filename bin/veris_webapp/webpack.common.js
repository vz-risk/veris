const path = require('path');
//const CleanWebpackPlugin = require('clean-webpack-plugin'); // removed to update clean-web-plugin to v3
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: {
    app: './src/js/main.js',
    css: './assets/css/dbir.css'
  },
  plugins: [
    //new CleanWebpackPlugin(['dist']),
    new CleanWebpackPlugin(), // Updated for clean-webpack-plugin v2 and v3
    new MiniCssExtractPlugin({
      filename: 'assets/css/[name].css',
      chunkFilename: '[id].css'
    }),
    new HtmlWebpackPlugin({
      title: 'VERIS Webapp',
      template: path.join(__dirname, 'assets', 'index.html')
    })
  ],
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist'),
    publicPath: "/"
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader'
        ]
      },
      {
        test: /\.m?js?$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
            plugins: [
              '@babel/plugin-transform-react-jsx',
              ['@babel/plugin-proposal-decorators', { "legacy": true }],
              ['@babel/plugin-proposal-class-properties', { "loose": true }],
            ]
          }
        }
      }
    ]
  },
  resolve: {
    fallback: {
        stream: false
    }
  }
};
