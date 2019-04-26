(function(c, a) {
    var b = function() {
        this.isInit = false;
        this.DrawManager;
        this.DrawOverlay;
        this.Point;
        this.Fill
    };
    b.prototype = {
        Init: function() {
            var d = this;
            if (d.isInit) {
                return d
            }
            d.isInit = true;
            if (!d.DrawManager) {
                d.DrawManager = d.DrawManager || new TGOS.TGDrawing();
                d.DrawManager.setMap(Tmap.getTMap());
                d.DrawManager.setOptions({
                    drawingControl: false,
                    drawingControlOptions: {
                        position: TGOS.TGControlPosition.BOTTOM_RIGHT
                    },
                    markerOptions: {
                        draggable: false,
                        flat: true,
                        zIndex: 1
                    }
                });
                d.DrawManager.setMarkerOptions({
                    icon: new TGOS.TGImage("../../Resources/Project/Images/blue/PointStatInfo.png", new TGOS.TGSize(33, 33), new TGOS.TGPoint(0, 0), new TGOS.TGPoint(17, 33)),
                    draggable: false,
                    flat: true,
                    zIndex: 1
                });
                TGOS.TGEvent.addListener(d.DrawManager, "marker_complete", function(f) {
                    d.DrawOverlay = f.overlay;
                    d.completePlacePoint(f.overlay.getPosition())
                })
            }
            a("#PointStatInfoBox_Tabs").tabs({
                activate: function(e, f) {
                    a("#PointStatInfoBox_Tabs_Title a").css({
                        color: "#555"
                    }).removeClass("PointStatInfoBox_Selected");
                    a(f.newTab[0]).find("a").css({
                        color: "#e40000"
                    }).addClass("PointStatInfoBox_Selected")
                },
                create: function(e, f) {
                    a(f.tab[0]).find("a").css({
                        color: "#e40000"
                    }).addClass("PointStatInfoBox_Selected")
                }
            });
            d.BindPointStatInfoBox_HeaderClose_Click();
            d.BindPointStatInfoBox_PlacePoint_Click();
            d.BindPointStatInfoBox_STUnitOneBt_Click();
            return d
        },
        BindPointStatInfoBox_HeaderClose_Click: function() {
            var d = this;
            a("#PointStatInfoBox_HeaderClose").click(function() {
                d.clearMap(true);
                d.close()
            })
        },
        BindPointStatInfoBox_PlacePoint_Click: function() {
            var d = this;
            a("#PointStatInfoBox_PlacePoint").click(function() {
                var e = a(this);
                if (e.val() == "選取位置") {
                    d.placePoint()
                } else {
                    d.cnacelPlacePoint()
                }
            })
        },
        BindPointStatInfoBox_STUnitOneBt_Click: function() {
            var d = this;
            a(".PointStatInfoBox_STUnitOneBt").click(function() {
                a(".PointStatInfoBox_STUnitOneBt").removeClass("PointStatInfoBox_Selected");
                d.clearUIResult();
                var e = a(this);
                var f = e.attr("code");
                var g = e.attr("data-stunit");
                if (f && g) {
                    a.ajax({
                        url: sirc.utility.getWebRootUrl() + "Generic/Project/GHSTATViewer.ashx",
                        type: "POST",
                        data: {
                            method: "GetPointGeometry",
                            code: f,
                            stunit: g
                        },
                        beforeSend: function() {}
                    }).done(function(i) {
                        var k = a.parseJSON(i);
                        if (k.Code == 1) {
                            try {
                                var h = util.parsePolyWkt(k.Content.geometry);
                                if (d.Fill) {
                                    d.Fill.setMap(null)
                                }
                                d.Fill = new TGOS.TGFill(Tmap.getTMap(), h, {
                                    fillColor: "#FFFF00",
                                    fillOpacity: 0.2,
                                    strokeColor: "#FF8000",
                                    strokeWeight: 5,
                                    strokeOpacity: 1
                                });
                                Tmap.View.zoomTo(d.Fill.getEnvelope());
                                Tmap.View.zoomTo(d.Fill.getEnvelope(), parseInt(Tmap.getTMap().getLevel()))
                            } catch (j) {}
                        }
                    }).fail(function(i, j, h) {}).always(function(h, j, i) {})
                }
                e.addClass("PointStatInfoBox_Selected");
                setTimeout(function() {
                    d.showLoading(function() {
                        try {
                            var h = e.parents(".PointStatInfoBox_Tabs_Item").find(".PointStatInfoBox_STUnitContent");
                            var s = a(".PointStatInfoBox_TabItem.PointStatInfoBox_Selected").data("division");
                            var I = e.data("stunit");
                            var O = a("#PointStatInfoBox_PointX").text();
                            var P = a("#PointStatInfoBox_PointY").text();
                            if (a.trim(O) == "" || a.trim(P) == "") {
                                alert("請先設定點位座標");
                                return
                            }
                            var J = window.pointinfo["divi" + s][I];
                            for (var G = 0, H = J.length; G < H; G++) {
                                var F = J[G];
                                switch (F.type) {
                                    case "table":
                                        var K = F.content;
                                        for (var v = 0, z = K.length; v < z; v++) {
                                            var B = K[v];
                                            d.getSTData(O, P, I, B.mdcode, B.colname, B.yearoffset, B, function(Q, p, i) {
                                                var S = p.times;
                                                var U = p[i];
                                                for (var x = 0, y = S.length; x < y; x++) {
                                                    var R = S[x];
                                                    Q.time = statMap.getSTTimeText(R);
                                                    if (U) {
                                                        var T = U[R];
                                                        Q.value = T;
                                                        Q.valuetext = statMap.commaformat(T)
                                                    } else {
                                                        Q.value = "-";
                                                        Q.valuetext = "-"
                                                    }
                                                }
                                            }, function(j, i) {
                                                j.value = "-";
                                                j.valuetext = "-";
                                                j.time = "-"
                                            }, false)
                                        }
                                        break;
                                    case "chart":
                                        var k = F.content;
                                        for (var v = 0, z = k.length; v < z; v++) {
                                            var B = k[v];
                                            var q = [];
                                            for (var D = 0, E = B.colnames.length; D < E; D++) {
                                                var C = B.colnames[D];
                                                q.push(C.colname)
                                            }
                                            d.getSTData(O, P, I, B.mdcode, q.join(","), B.yearoffset, B, function(U, y, x) {
                                                var W = y.times;
                                                var i = x.split(",");
                                                if (W.length == 1) {
                                                    var V = W[0];
                                                    for (var Q = 0, R = i.length; Q < R; Q++) {
                                                        var j = i[Q];
                                                        var Y = y[j][V];
                                                        var Z = statMap.commaformat(Y);
                                                        for (var S = 0, T = U.colnames.length; S < T; S++) {
                                                            var p = U.colnames[S];
                                                            if (p.colname == j) {
                                                                p.time = statMap.getSTTimeText(V);
                                                                p.value = Y;
                                                                p.valuetext = Z;
                                                                break
                                                            }
                                                        }
                                                    }
                                                } else {
                                                    U.timecolnames = [];
                                                    for (var Q = 0, R = i.length; Q < R; Q++) {
                                                        var j = i[Q];
                                                        var X = y[j];
                                                        for (var S = 0, T = W.length; S < T; S++) {
                                                            var V = W[S];
                                                            var Y = X[V];
                                                            var Z = statMap.commaformat(Y);
                                                            U.timecolnames.push({
                                                                colname: j,
                                                                displaytext: Z,
                                                                time: statMap.getSTTimeText(V),
                                                                value: Y
                                                            })
                                                        }
                                                    }
                                                }
                                            }, function(y, j) {
                                                for (var p = 0, x = y.colnames.length; p < x; p++) {
                                                    var i = y.colnames[p];
                                                    i.time = "-";
                                                    i.value = "-";
                                                    i.valuetext = "-"
                                                }
                                            }, false)
                                        }
                                        break
                                }
                            }
                            for (var G = 0, H = J.length; G < H; G++) {
                                var F = J[G];
                                var u = [];
                                switch (F.type) {
                                    case "table":
                                        var K = F.content;
                                        u.push('<div class="PointStatInfoBox_datagrid">');
                                        u.push("     <table >");
                                        u.push("         <thead>");
                                        u.push("             <tr >");
                                        u.push("                 <th >資料時間</th>");
                                        u.push("                 <th >資料項目</th>");
                                        u.push("                 <th >資料數值</th>");
                                        u.push("             </tr>");
                                        u.push("         </thead>");
                                        u.push("         <tbody>");
                                        for (var v = 0, z = K.length; v < z; v++) {
                                            var B = K[v];
                                            u.push('             <tr class="PointStatInfoBox_Row ' + ((v + 1) % 2 == 1 ? "alt" : "") + '">');
                                            u.push("                 <td >" + B.time + "</td>");
                                            u.push("                 <td >" + B.displaytext + "</td>");
                                            u.push("                 <td >" + B.valuetext + "</td>");
                                            u.push("             </tr>")
                                        }
                                        u.push("         </tbody>");
                                        u.push("     </table>");
                                        u.push("</div>");
                                        h.append(u.join(""));
                                        break;
                                    case "chart":
                                        var k = F.content;
                                        u = [];
                                        for (var v = 0, z = k.length; v < z; v++) {
                                            var B = k[v];
                                            var r = B.colnames;
                                            var o = !B.chartheight ? 450 : B.chartheight;
                                            var w = s + "_" + I + "_chart_" + B.type + "_" + G + "_" + v;
                                            h.append('<div id="' + w + '" style="width: 98%; padding:0px; height: ' + o + 'px; margin-top:12px;border: 1px solid #ccc; border-radius: 5px;"></div>');
                                            var L = "";
                                            for (var D = 0, E = r.length; D < E; D++) {
                                                var M = r[D];
                                                L = M.time
                                            }
                                            switch (B.type) {
                                                case "pie":
                                                    var N = B.mdtitle + ((L == "" || L == undefined) ? "" : ("\n(" + L + ")"));
                                                    var A = false;
                                                    if (B.valueunit == "百分比" || B.valueunit == "千分比" || B.valueunit == "%") {
                                                        A = true
                                                    }
                                                    var n = AmCharts.makeChart(w, {
                                                        type: "pie",
                                                        startDuration: 0,
                                                        theme: "light",
                                                        addClassNames: true,
                                                        marginLeft: 15,
                                                        marginRight: 15,
                                                        marginBottom: 0,
                                                        marginTop: 0,
                                                        radius: "30%",
                                                        labelText: "[[percents]]%",
                                                        labelRadius: 10,
                                                        balloonText: A ? ("[[title]]: [[percents]]% ") : ("[[title]]: [[percents]]%&nbsp;&nbsp;&nbsp;&nbsp;[[value]](" + B.valueunit + ")\n[[description]] "),
                                                        titles: [{
                                                            text: N,
                                                            size: 15
                                                        }],
                                                        legend: {
                                                            markerType: "circle",
                                                            position: "bottom",
                                                            marginBottom: 0,
                                                            autoMargins: false,
                                                            labelText: "[[title]]　　　",
                                                            valueText: "",
                                                            align: "center"
                                                        },
                                                        innerRadius: "0%",
                                                        defs: {
                                                            filter: [{
                                                                id: "shadow",
                                                                width: "200%",
                                                                height: "200%",
                                                                feOffset: {
                                                                    result: "offOut",
                                                                    "in": "SourceAlpha",
                                                                    dx: 0,
                                                                    dy: 0
                                                                },
                                                                feGaussianBlur: {
                                                                    result: "blurOut",
                                                                    "in": "offOut",
                                                                    stdDeviation: 5
                                                                },
                                                                feBlend: {
                                                                    "in": "SourceGraphic",
                                                                    in2: "blurOut",
                                                                    mode: "normal"
                                                                }
                                                            }]
                                                        },
                                                        dataProvider: r,
                                                        valueField: "value",
                                                        titleField: "displaytext",
                                                        "export": {
                                                            enabled: false
                                                        }
                                                    });
                                                    n.addListener("init", function() {
                                                        n.legend.addListener("rollOverItem", handleRollOver)
                                                    });
                                                    n.addListener("rollOverSlice", function(i) {
                                                        var j = i.dataItem.wedge.node;
                                                        j.parentNode.appendChild(j)
                                                    });
                                                    window.pointinfo.charts.push({
                                                        id: w,
                                                        chart: n
                                                    });
                                                    break;
                                                case "col":
                                                    var N = B.mdtitle + ((L == "" || L == undefined) ? "" : ("\n(" + L + ")"));
                                                    var l = AmCharts.makeChart(w, {
                                                        type: "serial",
                                                        theme: "light",
                                                        marginRight: 70,
                                                        dataProvider: r,
                                                        titles: [{
                                                            text: N,
                                                            size: 15
                                                        }],
                                                        valueAxes: [{
                                                            axisAlpha: 0,
                                                            position: "left",
                                                            title: B.displaytitle
                                                        }],
                                                        startDuration: 1,
                                                        graphs: [{
                                                            balloonText: "<b>[[category]]: [[value]](" + B.valueunit + ")</b>",
                                                            fillColorsField: "color",
                                                            fillAlphas: 0.9,
                                                            lineAlpha: 0.2,
                                                            type: "column",
                                                            valueField: "value"
                                                        }],
                                                        chartScrollbar: {
                                                            scrollbarHeight: 5,
                                                            backgroundAlpha: 0.1,
                                                            backgroundColor: "#868686",
                                                            selectedBackgroundColor: "#67b7dc",
                                                            selectedBackgroundAlpha: 1
                                                        },
                                                        chartCursor: {
                                                            categoryBalloonEnabled: false,
                                                            cursorAlpha: 0,
                                                            zoomable: false
                                                        },
                                                        categoryField: "displaytext",
                                                        categoryAxis: {
                                                            gridPosition: "start",
                                                            labelRotation: 45
                                                        },
                                                        "export": {
                                                            enabled: false
                                                        }
                                                    });
                                                    window.pointinfo.charts.push({
                                                        id: w,
                                                        chart: l
                                                    });
                                                    break;
                                                case "line":
                                                    var N = B.mdtitle;
                                                    var m = AmCharts.makeChart(w, {
                                                        type: "serial",
                                                        theme: "light",
                                                        legend: {
                                                            useGraphSettings: true,
                                                            valueText: ""
                                                        },
                                                        dataProvider: B.timecolnames,
                                                        titles: [{
                                                            text: N,
                                                            size: 15
                                                        }],
                                                        synchronizeGrid: true,
                                                        valueAxes: [{
                                                            id: "v1",
                                                            axisColor: "#FF6600",
                                                            axisThickness: 2,
                                                            axisAlpha: 1,
                                                            position: "left"
                                                        }],
                                                        graphs: [{
                                                            valueAxis: "v1",
                                                            lineColor: "#FF6600",
                                                            balloonText: "[[value]](" + B.valueunit + ")",
                                                            bullet: "round",
                                                            bulletBorderThickness: 1,
                                                            hideBulletsCount: 30,
                                                            title: B.displaytitle,
                                                            valueField: "value",
                                                            fillAlphas: 0
                                                        }],
                                                        chartScrollbar: {},
                                                        chartCursor: {
                                                            cursorPosition: "mouse"
                                                        },
                                                        categoryField: "time",
                                                        categoryAxis: {
                                                            parseDates: false,
                                                            axisColor: "#DADADA",
                                                            minorGridEnabled: true
                                                        },
                                                        "export": {
                                                            enabled: false
                                                        }
                                                    });
                                                    window.pointinfo.charts.push({
                                                        id: w,
                                                        chart: m
                                                    });
                                                    break
                                            }
                                        }
                                        break
                                }
                            }
                        } catch (t) {} finally {
                            d.hideLoading()
                        }
                    })
                }, 0)
            })
        },
        getSTData: function(k, l, i, h, e, m, g, j, f, d) {
            a.ajax({
                url: sirc.utility.getWebRootUrl() + "Generic/Project/GHSTATViewer.ashx",
                type: "POST",
                async: d == undefined ? true : d,
                data: {
                    method: "GetPointSTData",
                    x: k,
                    y: l,
                    mdcode: h,
                    stunit: i,
                    column: e,
                    yearoffset: m
                },
                beforeSend: function() {}
            }).done(function(n) {
                try {
                    var p = a.parseJSON(n);
                    console.log(p);
                    if (p.Code == 1) {
                        if (a.isFunction(j)) {
                            j(g, p.Content, e)
                        }
                    } else {
                        alert(p.Message);
                        if (a.isFunction(f)) {
                            f(g, e)
                        }
                    }
                } catch (o) {
                    if (a.isFunction(f)) {
                        f(g, e)
                    }
                } finally {}
            }).fail(function(o, p, n) {
                if (a.isFunction(f)) {
                    f(g, e)
                }
            }).always(function(n, p, o) {})
        },
        placePoint: function(f, g) {
            var d = this;
            d.clearUICondition();
            d.clearUIResult();
            if (!f && !g) {
                a("#PointStatInfoBox_PlacePoint").val("取消選取");
                a("#PointStatInfoBox_PointX").text("");
                a("#PointStatInfoBox_PointY").text("");
                a(".PointStatInfoBox_GEO_COUNTY").text("").prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", "");
                a(".PointStatInfoBox_GEO_TOWN").text("").prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", "");
                a(".PointStatInfoBox_GEO_VILLAGE").text("").prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", "");
                a(".PointStatInfoBox_GEO_CODE2").text("").prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", "");
                a(".PointStatInfoBox_GEO_CODE1").text("").prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", "");
                a(".PointStatInfoBox_GEO_CODEBASE").text("").prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", "");
                d.clearMap(true);
                d.DrawManager.enterMarkMode()
            } else {
                d.clearMap(true);
                var e = new TGOS.TGPoint(f, g);
                d.DrawOverlay = new TGOS.TGMarker(Tmap.getTMap(), e);
                d.DrawOverlay.setZIndex(1);
                d.DrawOverlay.setIcon(new TGOS.TGImage("../../Resources/Project/Images/blue/PointStatInfo.png", new TGOS.TGSize(33, 33), new TGOS.TGPoint(0, 0), new TGOS.TGPoint(17, 33)));
                d.DrawOverlay.setVisible(true);
                d.completePlacePoint(e)
            }
            return d
        },
        cnacelPlacePoint: function() {
            var d = this;
            a("#PointStatInfoBox_PlacePoint").val("選取位置");
            d.DrawManager.setDrawingMode(TGOS.TGOverlayType.NONE)
        },
        completePlacePoint: function(k) {
            var j = this;
            a("#PointStatInfoBox_PlacePoint").val("選取位置");
            j.DrawManager.setDrawingMode(TGOS.TGOverlayType.NONE);
            a("#PointStatInfoBox_PointX").text(k.x.toFixed(3));
            a("#PointStatInfoBox_PointY").text(k.y.toFixed(3));
            var g = a(".PointStatInfoBox_GEO_COUNTY");
            var h = a(".PointStatInfoBox_GEO_TOWN");
            var i = a(".PointStatInfoBox_GEO_VILLAGE");
            var e = a(".PointStatInfoBox_GEO_CODE2");
            var d = a(".PointStatInfoBox_GEO_CODE1");
            var f = a(".PointStatInfoBox_GEO_CODEBASE");
            a.ajax({
                url: sirc.utility.getWebRootUrl() + "Generic/Project/GHSTATViewer.ashx",
                type: "POST",
                data: {
                    method: "GetPointGEOInfo",
                    xy: k.x + " " + k.y
                },
                beforeSend: function() {
                    g.text("讀取中...").prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", "");
                    h.text("讀取中...").prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", "");
                    i.text("讀取中...").prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", "");
                    e.text("讀取中...").prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", "");
                    d.text("讀取中...").prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", "");
                    f.text("讀取中...").prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", "")
                }
            }).done(function(l) {
                try {
                    var o = a.parseJSON(l);
                    console.log(o);
                    if (o.Code == 1) {
                        if (o.ContentObject.length > 0) {
                            var n = o.ContentObject[0];
                            g.text(n.COUNTY).prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", n.COUNTY_ID);
                            h.text(n.TOWN).prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", n.TOWN_ID);
                            i.text(n.VILLAGE).prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", n.TOWN_ID + "-" + n.VILLAGE_ID);
                            e.text(n.CODE2).prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", n.CODE2);
                            d.text(n.CODE1).prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", n.CODE1);
                            f.text(n.CODEBASE).prev().find(".PointStatInfoBox_STUnitOneBt").attr("code", n.CODEBASE);
                            a(a(a(".PointStatInfoBox_TabItem")[0]).attr("href")).find('.PointStatInfoBox_STUnitOneBt[data-stunit="U01CO"]').click()
                        } else {
                            g.text("無資料...");
                            h.text("無資料...");
                            i.text("無資料...");
                            e.text("無資料...");
                            d.text("無資料...");
                            f.text("無資料...")
                        }
                    } else {
                        g.text("無資料...");
                        h.text("無資料...");
                        i.text("無資料...");
                        e.text("無資料...");
                        d.text("無資料...");
                        f.text("無資料...")
                    }
                } catch (m) {
                    g.text("無資料...");
                    h.text("無資料...");
                    i.text("無資料...");
                    e.text("無資料...");
                    d.text("無資料...");
                    f.text("無資料...")
                } finally {}
            }).fail(function(m, n, l) {
                g.text("無資料...");
                h.text("無資料...");
                i.text("無資料...");
                e.text("無資料...");
                d.text("無資料...");
                f.text("無資料...")
            }).always(function(l, n, m) {})
        },
        show: function() {
            var d = this;
            a("#PointStatInfoBox").show(function() {
                if (d.Box) {
                    d.Box.IsOpen = true
                }
                a("#PointStatInfoBox .Content").scrollTop(0)
            });
            return d
        },
        close: function() {
            var d = this;
            a("#PointStatInfoBox").hide();
            if (d.Box) {
                d.Box.IsOpen = false
            }
            return d
        },
        clearMap: function(e) {
            var d = this;
            a("#PointStatInfoBox_PlacePoint").val("選取位置");
            if (d.DrawManager) {
                d.DrawManager.setDrawingMode(TGOS.TGOverlayType.NONE)
            }
            if (d.DrawOverlay && e) {
                d.DrawOverlay.setMap(null);
                d.DrawOverlay = undefined
            }
            if (d.Fill) {
                d.Fill.setMap(null);
                d.Fill = undefined
            }
            Tmap.MessageBox.remove()
        },
        clearUIResult: function() {
            window.pointinfo.removecharts();
            a(".PointStatInfoBox_STUnitContent").empty()
        },
        clearUICondition: function() {
            a(a(".PointStatInfoBox_TabItem")[0]).click();
            a(".PointStatInfoBox_STUnitOneBt").removeClass("PointStatInfoBox_Selected");
            a(".PointStatInfoBox_GEO").text("")
        },
        showLoading: function(d) {
            a("#PointStatInfoBox_Loading").fadeIn(400, d)
        },
        hideLoading: function() {
            a("#PointStatInfoBox_Loading").fadeOut()
        }
    };
    c.PointStatInfoBoxInstance = c.PointStatInfoBoxInstance || sirc.Inherit.extend(new sirc.boxBase(), new b())
})(window, jQuery);
