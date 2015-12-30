module.exports = {
  entry: './js/app.js',
  output: {
    filename: 'public/js/llo-app.js'
  },
  module: {
    loaders: [
      { 
        test: /\.jsx?$/,
        loader: 'babel-loader',
        query: {
          "presets": ["es2015", "react"]
        },
        exclude: /(node_modules|bower_components)/
      },
      { test: /\.css$/, loader: 'style-loader!css-loader' },
    ]
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  }
};
