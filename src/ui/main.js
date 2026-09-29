Ext.namespace("SYNO.SDS.LibreSpeedTest");

// -----------------------------------------------------------------
// App entry point
// -----------------------------------------------------------------
Ext.define("SYNO.SDS._ThirdParty.App.LibreSpeedTest", {
    extend: "SYNO.SDS.AppInstance",
    appWindowName: "SYNO.SDS.LibreSpeedTest.MainWindow",
    constructor: function() {
        this.callParent(arguments);
    }
});

// -----------------------------------------------------------------
// Main window - embeds the existing LibreSpeed test page via iframe.
// index.html/speedtest.js already implement the full speedtest UI,
// so there's no need to rebuild it as Ext JS components; the window
// just hosts it at its served path under /webman/3rdparty/LibreSpeedTest/.
// -----------------------------------------------------------------
Ext.define("SYNO.SDS.LibreSpeedTest.MainWindow", {
    extend: "SYNO.SDS.AppWindow",

    IFRAME_SRC: "/webman/3rdparty/LibreSpeedTest/index.html",

    constructor: function(a) {
        this.appInstance = a.appInstance;
        SYNO.SDS.LibreSpeedTest.MainWindow.superclass.constructor.call(this, Ext.apply({
            layout: "fit",
            resizable: true,
            cls: "syno-app-win librespeedtest-win",
            maximizable: true,
            minimizable: true,
            showHelp: false,
            width: 720,
            height: 630,
            html: this.buildHtml(),
            listeners: {
                afterrender: {
                    fn: this.onAfterRender,
                    scope: this
                }
            }
        }, a));
    },

    buildHtml: function() {
        return [
            '<style>',
            '  .librespeedtest-body { display:flex; height:100%; }',
            '  .librespeedtest-frame { flex:1 1 auto; width:100%; height:100%; border:0; }',
            '</style>',
            '<div class="librespeedtest-body">',
            '  <iframe class="librespeedtest-frame" src="' + this.IFRAME_SRC + '"></iframe>',
            '</div>'
        ].join("");
    },

    onAfterRender: function() {
        var me = this;
        var el = this.body.dom;
        this.frameEl = el.querySelector(".librespeedtest-frame");
        var frame = this.frameEl;
        if (!frame) {
            return;
        }
        // Clicks inside the iframe never reach DSM's window manager, so forward them
        var attach = function() {
            try {
                frame.contentWindow.document.addEventListener("mousedown", function() {
                    me.toFront();
                }, true);
            } catch (e) {}
        };
        frame.addEventListener("load", attach);
        attach();
    },

    onClose: function() {
        SYNO.SDS.LibreSpeedTest.MainWindow.superclass.onClose.apply(this, arguments);
        this.doClose();
        return true;
    }
});
