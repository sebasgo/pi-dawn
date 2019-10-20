const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')

module.exports = {
    assetsDir: 'static',
    configureWebpack: {
        plugins: [
            new VuetifyLoaderPlugin()
        ],
    },
    devServer: {
        proxy: 'http://localhost:5000'
    }
};
