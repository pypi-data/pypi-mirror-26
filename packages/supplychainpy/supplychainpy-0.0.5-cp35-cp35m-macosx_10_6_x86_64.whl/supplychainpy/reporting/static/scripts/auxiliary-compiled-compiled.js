/**
 * Created by Fasusi on 22/05/2016.
 */
import $ from 'jquery';

$(function () {

    $('#loader').hide();
    $('#currency-dropdown-btn >li').click(function () {
        var currency = $(".dropdown-menu > li > a").text();
        $('#currency-dropdown-btn').text(currency);
    });

    $('div.nav-tab').hover(highlight);

    $('#search-btn').click(function () {
        $("#profile-rec").hide();
        $("#sku-rec > div").hide();
        search_recommendations();
    });

    $('#sim-search-btn').click(function () {
        $("#profile-rec").hide();
        $("#sim-sku-rec > div").hide();
        search_sim();
    });

    $('#simulate-btn').click(function () {
        $('<div id="loader">').show();
        run_simulation();
    });

    $('#clear-btn').click(function () {
        show_recommendations();
    });

    $('#sim-clear-btn').click(function () {
        show_sim();
    });

    $('#sim-detail-btn').click(function () {
        toggle_reporting_view_alt('[id$=sim-detail] > recommendation-panel');
    });

    $('#shortages-btn').click(function () {
        toggle_reporting_view('collapse-shortages');
    });

    $('#excess-btn').click(function () {
        toggle_reporting_view('collapse-excess');
    });

    $('#ses-btn').click(function () {
        toggle_reporting_view('ses-tg');
    });

    $('#htces-btn').click(function () {
        toggle_reporting_view('htces');
    });

    $('#chat-btn').click(function () {
        chat_to_bot();
    });

    $('#classifications-btn').click(function () {
        toggle_reporting_view('collapse-classification');
    });

    $('#search-input').keypress(function (event) {
        if (event.keyCode == 13) {
            $('#search-btn').click();
        }
    });

    $('#chat-input').keypress(function (event) {
        if (event.keyCode == 13) {
            $('#chat-btn').click();
        }
    });

    $('#runs-input').keypress(function (event) {
        if (event.keyCode == 13) {
            $('#simulate-btn').click();
        }
    });

    $('#sim-search-input').keypress(function (event) {
        if (event.keyCode == 13) {
            $('#sim-search-btn').click();
        }
    });
    load_currency_codes();
    // ajax request for json containing sku related. Is used to: builds revenue chart (#chart).
    var ay = [{
        "name": "abc_xyz_classification",
        "op": "eq",
        "val": "AY",
        "direction": "desc",
        "limit": 10
    }, { "name": "shortage_rank", "op": "le", "val": 100, "direction": "desc", "limit": 10, "results_per_page": 10 }];
    var ax = [{
        "name": "abc_xyz_classification",
        "op": "eq",
        "val": "AX",
        "direction": "desc",
        "limit": 10
    }, { "name": "shortage_rank", "op": "le", "val": 100, "direction": "desc", "limit": 10, "results_per_page": 10 }];
    var az = [{
        "name": "abc_xyz_classification",
        "op": "eq",
        "val": "AZ",
        "direction": "desc",
        "limit": 10
    }, { "name": "shortage_rank", "op": "le", "val": 100, "direction": "desc", "limit": 10, "results_per_page": 10 }];

    var bx = [{
        "name": "abc_xyz_classification",
        "op": "eq",
        "val": "BX",
        "direction": "desc",
        "limit": 10
    }, { "name": "shortage_rank", "op": "le", "val": 100, "direction": "desc", "limit": 10, "results_per_page": 10 }];

    var by = [{
        "name": "abc_xyz_classification",
        "op": "eq",
        "val": "BY",
        "direction": "desc",
        "limit": 10
    }, { "name": "shortage_rank", "op": "le", "val": 100, "direction": "desc", "limit": 10, "results_per_page": 10 }];

    var bz = [{
        "name": "abc_xyz_classification",
        "op": "eq",
        "val": "BZ",
        "direction": "desc",
        "limit": 10
    }, { "name": "shortage_rank", "op": "le", "val": 100, "direction": "desc", "limit": 10, "results_per_page": 10 }];

    var cx = [{
        "name": "abc_xyz_classification",
        "op": "eq",
        "val": "CX",
        "direction": "desc",
        "limit": 10
    }, { "name": "shortage_rank", "op": "le", "val": 100, "direction": "desc", "limit": 10, "results_per_page": 10 }];

    var cy = [{
        "name": "abc_xyz_classification",
        "op": "eq",
        "val": "CY",
        "direction": "desc",
        "limit": 10
    }, { "name": "shortage_rank", "op": "le", "val": 100, "direction": "desc", "limit": 10, "results_per_page": 10 }];

    var cz = [{
        "name": "abc_xyz_classification",
        "op": "eq",
        "val": "cz",
        "direction": "desc",
        "limit": 10
    }, { "name": "shortage_rank", "op": "le", "val": 100, "direction": "desc", "limit": 10, "results_per_page": 10 }];

    var filters = [{
        "name": "shortage_rank",
        "op": "le",
        "val": 10,
        "direction": "desc",
        "limit": 10,
        "results_per_page": 10
    }];
    var excess_filters = [{ "name": "excess_cost", "op": "gt", "val": 0, "direction": "desc", "limit": 10 }];

    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: '/reporting/api/v1.0/top_shortages',
        dataType: 'json',
        async: true,
        data: { "q": JSON.stringify({ "filters": filters }) },
        success: function (data) {
            console.log(data.json_list);
            //var currency_code = data.objects[i].currency.currency_code;
            //currency_fetch(currency_code);
            //create_shortages_table(data);
            render_shortages_chart(data, '#shortage-chart');
        },
        error: function (result) {

            console.log(result);
        }
    });
    //build force node graph on classification view page, is dependent on jinja template logic inserting a tag on the page
    //to identify what classification view has been triggered.
    var ay_val = $('#AY-node').length;
    var ax_val = $('#AX-node').length;
    var az_val = $('#AZ-node').length;
    var bx_val = $('#BX-node').length;
    var by_val = $('#BY-node').length;
    var bz_val = $('#BZ-node').length;
    var cx_val = $('#CX-node').length;
    var cy_val = $('#CY-node').length;
    var cz_val = $('#CZ-node').length;

    //console.log(ax_val);
    if (ay_val > 0) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/inventory_analysis',
            dataType: 'json',
            async: true,
            data: { "q": JSON.stringify({ "filters": ay }) },
            success: function (data) {
                //console.log(data.objects);
                var node_chart = new RenderForceChart(data, '#node-chart');
                node_chart.classification_force();
            },
            error: function (result) {}
        });
    }
    if (ax_val > 0) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/inventory_analysis',
            dataType: 'json',
            async: true,
            data: { "q": JSON.stringify({ "filters": ax }) },
            success: function (data) {
                //console.log(data.objects);
                if (data != null) {
                    var node_chart2 = new RenderForceChart(data, '#node-chart');
                    node_chart2.classification_force();
                }
            },
            error: function (result) {}
        });
    }
    if (az_val > 0) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/inventory_analysis',
            dataType: 'json',
            async: true,
            data: { "q": JSON.stringify({ "filters": az }) },
            success: function (data) {
                //console.log(data.objects);
                if (data != null) {
                    var node_chart2 = new RenderForceChart(data, '#node-chart');
                    node_chart2.classification_force();
                }
            },
            error: function (result) {}
        });
    }
    if (bx_val > 0) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/inventory_analysis',
            dataType: 'json',
            async: true,
            data: { "q": JSON.stringify({ "filters": bx }) },
            success: function (data) {
                //console.log(data.objects);
                if (data != null) {
                    var node_chart2 = new RenderForceChart(data, '#node-chart');
                    node_chart2.classification_force();
                }
            },
            error: function (result) {}
        });
    }

    if (by_val > 0) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/inventory_analysis',
            dataType: 'json',
            async: true,
            data: { "q": JSON.stringify({ "filters": by }) },
            success: function (data) {
                //console.log(data.objects);
                if (data != null) {
                    var node_chart2 = new RenderForceChart(data, '#node-chart');
                    node_chart2.classification_force();
                }
            },
            error: function (result) {}
        });
    }
    if (bz_val > 0) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/inventory_analysis',
            dataType: 'json',
            async: true,
            data: { "q": JSON.stringify({ "filters": bz }) },
            success: function (data) {
                //console.log(data.objects);
                if (data != null) {
                    var node_chart2 = new RenderForceChart(data, '#node-chart');
                    node_chart2.classification_force();
                }
            },
            error: function (result) {}
        });
    }
    if (cx_val > 0) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/inventory_analysis',
            dataType: 'json',
            async: true,
            data: { "q": JSON.stringify({ "filters": cx }) },
            success: function (data) {
                //console.log(data.objects);
                if (data != null) {
                    var node_chart2 = new RenderForceChart(data, '#node-chart');
                    node_chart2.classification_force();
                }
            },
            error: function (result) {}
        });
    }
    if (cy_val > 0) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/inventory_analysis',
            dataType: 'json',
            async: true,
            data: { "q": JSON.stringify({ "filters": cy }) },
            success: function (data) {
                //console.log(data.objects);
                if (data != null) {
                    var node_chart2 = new RenderForceChart(data, '#node-chart');
                    node_chart2.classification_force();
                }
            },
            error: function (result) {}
        });
    }
    if (cz_val > 0) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/inventory_analysis',
            dataType: 'json',
            async: true,
            data: { "q": JSON.stringify({ "filters": cz }) },
            success: function (data) {
                //console.log(data.objects);
                if (data != null) {
                    var node_chart2 = new RenderForceChart(data, '#node-chart');
                    node_chart2.classification_force();
                }
            },
            error: function (result) {}
        });
    }
    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: '/api/inventory_analysis',
        dataType: 'json',
        async: true,

        data: { "q": JSON.stringify({ "filters": excess_filters }) },
        success: function (data) {
            //console.log(data.objects);
            create_excess_table(data);
        },
        error: function (result) {}
    });

    //ajax request for json containing all costs summarised by product class (abcxyz), builds pie chart (#chart2)
    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: '/reporting/api/v1.0/abc_summary',
        dataType: 'json',
        async: true,
        data: "{}",
        success: function (data) {
            //console.log(data);
            var pie_chart1 = new RenderPieChart(data, '#pie-shortage');
            pie_chart1.shortages();
            var pie_chart2 = new RenderPieChart(data, '#excess-pie');
            pie_chart2.excess();
            create_classification_table(data);
            var pie_chart3 = new RenderPieChart(data, '#revenue-class-chart');
            pie_chart3.classification('revenue');
            var pie_chart4 = new RenderPieChart(data, '#shortage-class-chart');
            pie_chart4.classification('shortage');
            var pie_chart5 = new RenderPieChart(data, '#excess-class-chart');
            pie_chart5.classification('excess');
        },
        error: function (result) {
            //console.log(result);// make 404.html page
        }
    });

    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: '/reporting/api/v1.0/top_excess/10',
        dataType: 'json',
        async: true,
        data: "{}",
        success: function (data) {
            //console.log(data);
            render_excess_chart(data, '#excess-chart');
        },
        error: function (result) {
            //console.log(result);// make 404.html page
        }
    });

    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: '/api/forecast_breakdown',
        dataType: 'json',
        async: true,
        data: "{}",
        success: function (data) {
            //console.log(data);
            //console.log(data);

        },
        error: function (result) {
            //console.log(result);// make 404.html page
        }
    });

    bar_chart_sku();
    line_chart_forecast();
    line_chart_forecast_ses();
});

/** Searches for sku on recommendation page (feed.html)
 *  @function search_recommendations */
function search_recommendations() {

    var message = $('#search-input').val();
    show_search(message);
}

function search_sim() {

    var message = $('#sim-search-input').val();
    show_search(message);
}

function show_search(message) {
    $("#" + message.trim()).show();
}

function show_recommendations() {
    $('#search-input').val('');
    $("#profile-rec").show(500, "linear");
    $("#sku-rec > div").show().slideDown(600);
}

function show_sim() {

    $('#sim-search-input').val('');
    $("#sim-profile-rec").show(500, "linear");
    $("#sim-sku-rec > div").show().slideDown(600);
}

function run_simulation() {
    var runs = $('#runs-input').val();

    window.location = '/simulation/' + runs;
}

function chat_to_bot() {
    var user = 'You';
    var message = $('#chat-input').val();
    //console.log(message);
    render_bot_response(message, user);

    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: '/chat/' + message,
        dataType: 'json',
        async: true,
        data: "{}",
        success: function (data) {
            var communicator = 'Dash';
            render_bot_response(data, communicator);
            //console.log(data);
        },
        error: function (result) {

            //console.log(result);// make 404.html page
        }
    });

    $('#chat-input').val('');
}

function render_bot_response(message, communicator) {

    switch (communicator) {
        case 'You':

            $('<p style=\"color:#042029;\">' + communicator + ': ' + message + '</p><br><p></p>').insertAfter('#response-panel p:last').fadeIn("slow");

            break;
        case 'Dash':
            for (i = 0; i < message.json_list.length; i++) {
                if (message.json_list[i] != null && message.json_list[i] != '') {
                    $('<p style=\"color:#a2e1f6;\">' + communicator + ': ' + message.json_list[i] + '</p><br><p></p>').hide().insertAfter('#response-panel p:last').delay(800).fadeIn(1000);
                    $("#response-panel").animate({ scrollTop: $('#response-panel').prop("scrollHeight") }, 500);
                    ;
                }
            }

            break;
    }
}

function bar_chart_sku() {
    var orders_data = document.getElementById("orders-data");
    //console.log(orders_data.getElementsByClassName("orders-raw-data"));
    var wins = [];
    var period = [];

    for (i = 0; i < orders_data.getElementsByClassName("orders-raw-data").length; i++) {

        wins.push([i + 1, parseInt(orders_data.getElementsByClassName("orders-raw-data")[i].innerText)]);
        period.push([i + 1, i + 1]);
        //console.log(wins);
    }
    wins = [wins];
    //console.log(period);

    Flotr.draw(document.getElementById("demand-chart"), wins, {
        bars: {
            show: true,
            barWidth: 0.5
        },
        yaxis: {
            min: 0,
            tickDecimals: 0
        },
        xaxis: {
            ticks: period
        }
    });
}

function line_chart_forecast() {
    var orders_data = document.getElementById("orders-data");
    var forecast_data = document.getElementById("forecast-data");
    var forecast_values = document.getElementById("forecast");
    var safety_stock = document.getElementById("safety-stock");
    var reorder_lvl = document.getElementById("reorder-lvl");

    //console.log(safety_stock.innerText);
    var forecast = [];
    var orders = [];
    var regression = [];
    var safety = [];
    var reorder = [];

    for (i = 0; i < forecast_data.getElementsByClassName("forecast-raw-data").length; i++) {

        safety.push([i + 1, parseInt(safety_stock.innerText)]);
        reorder.push([i + 1, parseInt(reorder_lvl.innerText)]);
    }

    for (i = 0; i < forecast_data.getElementsByClassName("forecast-raw-data").length; i++) {

        forecast.push([i + 1, parseInt(forecast_data.getElementsByClassName("forecast-raw-data")[i].innerText)]);
    }

    for (i = 0; i < orders_data.getElementsByClassName("orders-raw-data").length; i++) {

        orders.push([i + 1, parseInt(orders_data.getElementsByClassName("orders-raw-data")[i].innerText)]);
    }

    //for (i = 0; i < forecast_values.getElementsByClassName("forecast-values").length; i++) {
    //
    //    forecast.push([forecast.length + i, parseInt(forecast_values.getElementsByClassName("forecast-values")[i].innerText)]);
    //
    //}

    for (i = 0; i < forecast_data.getElementsByClassName("regression").length; i++) {

        regression.push([i + 1, parseInt(forecast_data.getElementsByClassName("regression")[i].innerText)]);
    }

    //console.log(forecast);
    //console.log(wins);

    Flotr.draw(document.getElementById("forecast-chart"), [{
        data: orders,
        lines: { show: true },
        label: "orders"

    }, {
        data: forecast,
        lines: { show: true },
        label: "one-step forecast"
    }, {
        data: regression,
        lines: { show: true },
        label: "regression"
    }, {
        data: safety,
        lines: { show: true },
        label: "safety stock level",
        color: "#C61C6F"
    }, {
        data: reorder,
        lines: { show: true },
        label: "reorder level"
    }]);
}

function line_chart_forecast_ses() {
    var orders_data = document.getElementById("orders-data");
    console.log(orders_data);
    var forecast_data = document.getElementById("ses-data");
    var forecast_values = document.getElementById("ses");
    var safety_stock = document.getElementById("safety-stock");
    var reorder_lvl = document.getElementById("reorder-lvl");

    //console.log(safety_stock.innerText);
    var forecast = [];
    var orders = [];
    var regression = [];
    var safety = [];
    var reorder = [];

    for (i = 0; i < forecast_data.getElementsByClassName("forecast-raw-data-ses").length; i++) {

        safety.push([i + 1, parseInt(safety_stock.innerText)]);
        reorder.push([i + 1, parseInt(reorder_lvl.innerText)]);
    }

    for (i = 0; i < forecast_data.getElementsByClassName("forecast-raw-data-ses").length; i++) {

        forecast.push([i + 1, parseInt(forecast_data.getElementsByClassName("forecast-raw-data-ses")[i].innerText)]);
    }

    for (i = 0; i < orders_data.getElementsByClassName("orders-raw-data").length; i++) {

        orders.push([i + 1, parseInt(orders_data.getElementsByClassName("orders-raw-data")[i].innerText)]);
    }

    for (i = 0; i < forecast_data.getElementsByClassName("regression-ses").length; i++) {

        regression.push([i + 1, parseInt(forecast_data.getElementsByClassName("regression-ses")[i].innerText)]);
    }

    //console.log(forecast);
    //console.log(wins);

    Flotr.draw(document.getElementById("ses-chart"), [{
        data: orders,
        lines: { show: true },
        label: "orders"

    }, {
        data: forecast,
        lines: { show: true },
        label: "one-step forecast"
    }, {
        data: regression,
        lines: { show: true },
        label: "regression"
    }, {
        data: safety,
        lines: { show: true },
        label: "safety stock level",
        color: "#C61C6F"
    }, {
        data: reorder,
        lines: { show: true },
        label: "reorder level"
    }]);
}

function format_number(num) {
    return num.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
}

// helper functions for unpacking data from ajax requests
var unpack = {
    attribute_enum: {
        revenue: 'revenue',
        shortage_cost: 'shortage_cost',
        shortages: 'shortages'

    },

    sku_detail: function (data, value) {
        var barData = [];
        var tempData;
        var key;
        var i;
        for (key in data) {
            tempData = data[key];
            //console.log(tempData);
            for (i in tempData) {
                //.log(tempData[i].revenue);
                switch (value) {
                    case unpack.attribute_enum.revenue:
                        barData.push(tempData[i].revenue);
                        //console.log(barData);
                        break;
                    case upack.attribute_enum.shoratge_cost:
                        barData.push(tempData[i].shoratge_cost);
                }
            }
        }
        return barData;
    },

    excess: function (data, target) {
        var excess_data = [];
        var tempData;
        var key;
        for (key in data) {
            tempData = data[key];
            //console.log(tempData);
            for (i in tempData) {
                //console.log(tempData[i]);
                switch (target) {

                    case 'chart':
                        excess_data.push([tempData[i].abc_xyz_classification, tempData[i].total_excess]);
                        //console.log (excess_data);
                        break;

                    case 'table':
                        excess_data.push(tempData[i]);
                        //console.log(excess_data);
                        break;
                }
            }
        }
        return excess_data;
    },

    pie: function (data) {
        var pieData = [];
        var tempData;
        var key;

        for (key in data) {
            tempData = data[key];
            //console.log(tempData);
            for (i in tempData) {
                //console.log(tempData[i]);
                pieData.push([tempData[i].abc_xyz_classification, tempData[i].total_shortages]);
                //onsole.log(pieData);
            }
        }
        return pieData;
    },

    shortages: function (data, target) {
        var shortages_data = [];
        var tempData;
        var key;
        var i;
        for (key in data) {
            tempData = data[key];
            //console.log(tempData);
            for (i in tempData) {
                //console.log(tempData[i]);
                switch (target) {

                    case 'chart':
                        shortages_data.push([tempData[i].sku_id, tempData[i].shortage_cost]);
                        //console.log(shortages_data);
                        break;

                    case 'table':
                        shortages_data.push(tempData[i]);
                        //console.log(shortages_data);
                        break;
                }
            }
        }
        return shortages_data;
    },
    excess_cost: function (data, target) {
        var excess_data = [];
        var tempData;
        var key;
        var i;
        for (key in data) {
            tempData = data[key];
            //console.log(tempData);
            for (i in tempData) {
                //console.log(tempData[i]);
                switch (target) {

                    case 'chart':
                        excess_data.push([tempData[i].sku_id, tempData[i].excess_cost]);
                        //console.log(shortages_data);
                        break;

                    case 'table':
                        excess_data.push(tempData[i]);
                        //console.log(shortages_data);
                        break;
                }
            }
        }
        return excess_data;
    },

    excess_by_class: function (data, target, classification) {
        var excess_data = [];
        var tempData;
        var key;
        for (key in data) {
            tempData = data[key];
            //console.log(tempData[0]);
            for (i in tempData) {
                //console.log(tempData[i]);
                switch (target) {

                    case 'chart':
                        switch (classification) {
                            case 'AY':
                                if (tempData[i].abc_xyz_classification == 'AY') {
                                    excess_data.push([['excess', tempData[i].total_excess], ['revenue', tempData[i].total_revenue], ['shortage', tempData[i].total_shortages]]);
                                }
                        }
                        //console.log (excess_data);
                        break;

                    case 'table':
                        excess_data.push(tempData[i]);
                        //console.log(excess_data);
                        break;
                }
            }
        }
        //console.log(excess_data);
        return excess_data;
    },

    abc_xyz: function abc_xyz(data, target) {
        var abcxyz_data = [];
        var tempData;
        var key;
        var i;
        for (key in data) {
            tempData = data[key];
            //console.log(tempData);
            for (i in tempData) {
                //console.log(tempData[i]);
                switch (target) {

                    case 'chart':
                        abcxyz_data.push([tempData[i].sku_id, tempData[i].shortage_cost]);
                        //console.log(shortages_data);
                        break;

                    case 'table':
                        abcxyz_data.push(tempData[i]);
                        //console.log(shortages_data);
                        break;
                }
            }
        }
        return abcxyz_data;
    },

    classification: function classification(data, target) {
        var tempData;
        var key;
        var classification_data = [];
        var i;
        for (key in data) {
            tempData = data[key];
            //console.log(tempData);
            for (i in tempData) {
                //console.log(tempData[i]);
                switch (target) {

                    case 'revenue':
                        classification_data.push([tempData[i].abc_xyz_classification, tempData[i].total_revenue]);
                        //console.log(classification_data);
                        break;

                    case 'shortage':
                        classification_data.push([tempData[i].abc_xyz_classification, tempData[i].total_shortages]);
                        //console.log(classification_data);
                        break;

                    case 'excess':
                        classification_data.push([tempData[i].abc_xyz_classification, tempData[i].total_excess]);
                        //console.log(classification_data);
                        break;
                }
            }
        }
        return classification_data;
    }

};

//loads the currency codes into dropdown
function load_currency_codes() {
    var currency_symbols = [["AED", "United Arab Emirates Dirham"], ["AFN", "Afghanistan Afghani"], ["ALL", "Albania Lek"], ["AMD", "Armenia Dram"], ["ANG", "Netherlands Antilles Guilder"], ["AOA", "Angola Kwanza"], ["ARS", "Argentina Peso"], ["AUD", "Australia Dollar"], ["AWG", "Aruba Guilder"], ["AZN", "Azerbaijan New Manat"], ["BAM", "Bosnia and Herzegovina Convertible Marka"], ["BBD", "Barbados Dollar"], ["BDT", "Bangladesh Taka"], ["BGN", "Bulgaria Lev"], ["BHD", "Bahrain Dinar"], ["BIF", "Burundi Franc"], ["BMD", "Bermuda Dollar"], ["BND", "Brunei Darussalam Dollar"], ["BOB", "Bolivia Bolíviano"], ["BRL", "Brazil Real"], ["BSD", "Bahamas Dollar"], ["BTN", "Bhutan Ngultrum"], ["BWP", "Botswana Pula"], ["BYR", "Belarus Ruble"], ["BZD", "Belize Dollar"], ["CAD", "Canada Dollar"], ["CDF", "Congo/Kinshasa Franc"], ["CHF", "Switzerland Franc"], ["CLP", "Chile Peso"], ["CNY", "China Yuan Renminbi"], ["COP", "Colombia Peso"], ["CRC", "Costa Rica Colon"], ["CUC", "Cuba Convertible Peso"], ["CUP", "Cuba Peso"], ["CVE", "Cape Verde Escudo"], ["CZK", "Czech Republic Koruna"], ["DJF", "Djibouti Franc"], ["DKK", "Denmark Krone"], ["DOP", "Dominican Republic Peso"], ["DZD", "Algeria Dinar"], ["EGP", "Egypt Pound"], ["ERN", "Eritrea Nakfa"], ["ETB", "Ethiopia Birr"], ["EUR", "Euro Member Countries"], ["FJD", "Fiji Dollar"], ["FKP", "Falkland Islands (Malvinas) Pound"], ["GBP", "United Kingdom Pound"], ["GEL", "Georgia Lari"], ["GGP", "Guernsey Pound"], ["GHS", "Ghana Cedi"], ["GIP", "Gibraltar Pound"], ["GMD", "Gambia Dalasi"], ["GNF", "Guinea Franc"], ["GTQ", "Guatemala Quetzal"], ["GYD", "Guyana Dollar"], ["HKD", "Hong Kong Dollar"], ["HNL", "Honduras Lempira"], ["HRK", "Croatia Kuna"], ["HTG", "Haiti Gourde"], ["HUF", "Hungary Forint"], ["IDR", "Indonesia Rupiah", "ILS", "Israel Shekel"], ["IMP", "Isle of Man Pound"], ["INR", "India Rupee"], ["IQD", "Iraq Dinar"], ["IRR", "Iran Rial"], ["ISK", "Iceland Krona"], ["JEP", "Jersey Pound"], ["JMD", "Jamaica Dollar"], ["JOD", "Jordan Dinar"], ["JPY", "Japan Yen"], ["KES", "Kenya Shilling"], ["KGS", "Kyrgyzstan Som"], ["KHR", "Cambodia Riel"], ["KMF", "Comoros Franc"], ["KPW", "Korea (North) Won"], ["KRW", "Korea (South) Won"], ["KWD", "Kuwait Dinar"], ["KYD", "Cayman Islands Dollar"], ["KZT", "Kazakhstan Tenge"], ["LAK:", "Laos Kip"], ["LBP", "Lebanon Pound"], ["LKR", "Sri Lanka Rupee"], ["LRD", "Liberia Dollar"], ["LSL", "Lesotho Loti"], ["LYD", "Libya Dinar"], ["MAD", "Morocco Dirham"], ["MDL", "Moldova Leu"], ["MGA", "Madagascar Ariary"], ["MKD", "Macedonia Denar"], ["MMK", "Myanmar (Burma) Kyat"], ["MNT", "Mongolia Tughrik"], ["MOP", "Macau Pataca"], ["MRO", "Mauritania Ouguiya"], ["MUR", "Mauritius Rupee"], ["MVR", "Maldives (Maldive Islands) Rufiyaa"], ["MWK", "Malawi Kwacha"], ["MXN", "Mexico Peso"], ["MYR", "Malaysia Ringgit"], ["MZN", "Mozambique Metical"], ["NAD", "Namibia Dollar"], ["NGN", "Nigeria Naira"], ["NIO", "Nicaragua Cordoba"], ["NOK:", "Norway Krone"], ["NPR", "Nepal Rupee"], ["NZD", "New Zealand Dollar"], ["OMR", "Oman Rial"], ["PAB", "Panama Balboa"], ["PEN", "Peru Sol"], ["PGK", "Papua New Guinea Kina"], ["PHP", "Philippines Peso"], ["PKR", "Pakistan Rupee"], ["PLN", "Poland Zloty"], ["PYG", "Paraguay Guarani"], ["QAR", "Qatar Riyal"], ["RON", "Romania New Leu"], ["RSD", "Serbia Dinar"], ["RUB", "Russia Ruble"], ["RWF", "Rwanda Franc"], ["SAR", "Saudi Arabia Riyal"], ["SBD", "Solomon Islands Dollar"], ["SCR", "Seychelles Rupee"], ["SDG", "Sudan Pound"], ["SEK", "Sweden Krona"], ["SGD", "Singapore Dollar"], ["SHP", "Saint Helena Pound"], ["SLL", "Sierra Leone Leone"], ["SOS", "Somalia Shilling"], ["SPL:", "Seborga Luigino"], ["SR:D", "Suriname Dollar"], ["STD", "São Tomé and Príncipe Dobra"], ["SVC", "El Salvador Colon"], ["SYP", "Syria Pound"], ["SZL", "Swaziland Lilangeni"], ["THB", "Thailand Baht"], ["TJS", "Tajikistan Somoni"], ["TMT", "Turkmenistan Manat"], ["TND", "Tunisia Dinar"], ["TOP", "Tonga Pa'anga"], ["TRY", "Turkey Lira"], ["TTD", "Trinidad and Tobago Dollar"], ["TVD", "Tuvalu Dollar"], ["TWD", "Taiwan New Dollar"], ["TZS", "Tanzania Shilling"], ["UAH", "Ukraine Hryvnia"], ["UGX", "Uganda Shilling"], ["USD", "American Dollars"], ["UYU", "Uruguay Peso"], ["UZS", "Uzbekistan Som"], ["VEF", "Venezuela Bolivar"], ["VND", "Viet Nam Dong"], ["VUV", "Vanuatu Vatu"], ["WST", "Samoa Tala"], ["XAF", "Communauté Financière Africaine (BEAC) CFA Franc BEAC"], ["XCD", "East Caribbean Dollar"], ["XDR", "International Monetary Fund (IMF) Special Drawing Rights"], ["XOF", "Communauté Financière Africaine (BCEAO) Franc"], ["XPF", "Comptoirs Français du Pacifique (CFP) Franc"], ["YER", "Yemen Rial"], ["ZAR", "South Africa Rand"], ["ZMW", "Zambia Kwacha"], ["ZWD", "Zimbabwe Dollar"]];
    for (var i = 0; i < currency_symbols.length; i++) {
        //console.log(currency_symbols[i][0]);
        $("<li role=\"presentation\"><a role=\"menuitem\" class =\"text-center\" tabindex=\"-1\" href=\"#\">" + currency_symbols[i][0] + "</a></li>").insertAfter("#currency-list li:last");
    }
}

function highlight() {

    $(this).toggleClass('highlight-event');
}

function toggle_reporting_view(id) {
    $('#' + id).toggle("slow");
}

function toggle_reporting_view_alt(id) {
    $(id).toggle("slow");
}

function currency_fetch(id) {

    var filters = [{ "name": "id", "op": "eq", "val": id, "direction": "asc", "limit": 1 }];

    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: '/api/currency',
        dataType: 'json',
        async: true,
        data: { "q": JSON.stringify({ "filters": filters }) },
        success: function (data) {
            //console.log(JSON.stringify({"filters": filters}));
            //console.log(data);
            var li = [...data.objects];
            //console.log(li[0].currency_code);
            $('#currency-code').text(li[0].currency_code);
            return li[0].currency_code;
        },
        error: function (result) {}
    });
}

function currency_symbol_allocator(currency_symbol) {
    var currency_symbols = {
        "AED": "&#92;&#117;&#48;&#54;&#50;&#102;&#46;", "AFN": "&#1547;", "ALL": "Albania Lek",
        "AMD": "&#1423;", "ANG": "&#402;", "AOA": "Angola Kwanza",
        "ARS": "Argentina Peso", "AUD": "Australia Dollar", "AWG": "Aruba Guilder",
        "AZN": "Azerbaijan New Manat", "BAM": "Bosnia and Herzegovina Convertible Marka",
        "BBD": "Barbados Dollar", "BDT": "Bangladesh Taka", "BGN": "Bulgaria Lev", "BHD": "Bahrain Dinar",
        "BIF": "Burundi Franc", "BMD": "Bermuda Dollar", "BND": "Brunei Darussalam Dollar",
        "BOB": "Bolivia Bolíviano", "BRL": "Brazil Real", "BSD": "Bahamas Dollar",
        "BTN": "Bhutan Ngultrum", "BWP": "Botswana Pula", "BYR": "Belarus Ruble", "BZD": "Belize Dollar",
        "CAD": "Canada Dollar", "CDF": "Congo/Kinshasa Franc", "CHF": "Switzerland Franc",
        "CLP": "Chile Peso", "CNY": "China Yuan Renminbi", "COP": "Colombia Peso",
        "CRC": "Costa Rica Colon", "CUC": "Cuba Convertible Peso", "CUP": "Cuba Peso",
        "CVE": "Cape Verde Escudo", "CZK": "Czech Republic Koruna", "DJF": "Djibouti Franc",
        "DKK": "Denmark Krone", "DOP": "Dominican Republic Peso", "DZD": "Algeria Dinar",
        "EGP": "Egypt Pound", "ERN": "Eritrea Nakfa", "ETB": "Ethiopia Birr",
        "EUR": "&#8364;", "FJD": "Fiji Dollar", "FKP": "Falkland Islands (Malvinas) Pound",
        "GBP": "United Kingdom Pound", "GEL": "Georgia Lari", "GGP": "Guernsey Pound",
        "GHS": "Ghana Cedi", "GIP": "Gibraltar Pound", "GMD": "Gambia Dalasi", "GNF": "Guinea Franc",
        "GTQ": "Guatemala Quetzal", "GYD": "Guyana Dollar", "HKD": "Hong Kong Dollar",
        "HNL": "Honduras Lempira", "HRK": "Croatia Kuna", "HTG": "Haiti Gourde", "HUF": "Hungary Forint",
        "IDR": "Indonesia Rupiah", "ILS": "Israel Shekel", "IMP": "Isle of Man Pound",
        "INR": "India Rupee", "IQD": "Iraq Dinar", "IRR": "Iran Rial", "ISK": "Iceland Krona",
        "JEP": "Jersey Pound", "JMD": "Jamaica Dollar", "JOD": "Jordan Dinar", "JPY": "Japan Yen",
        "KES": "Kenya Shilling", "KGS": "Kyrgyzstan Som", "KHR": "Cambodia Riel", "KMF": "Comoros Franc",
        "KPW": "Korea (North) Won", "KRW": "Korea (South) Won", "KWD": "Kuwait Dinar",
        "KYD": "Cayman Islands Dollar", "KZT": "Kazakhstan Tenge", "LAK:": "Laos Kip",
        "LBP": "Lebanon Pound", "LKR": "Sri Lanka Rupee", "LRD": "Liberia Dollar", "LSL": "Lesotho Loti",
        "LYD": "Libya Dinar", "MAD": "Morocco Dirham", "MDL": "Moldova Leu", "MGA": "Madagascar Ariary",
        "MKD": "Macedonia Denar", "MMK": "Myanmar (Burma) Kyat", "MNT": "Mongolia Tughrik",
        "MOP": "Macau Pataca", "MRO": "Mauritania Ouguiya", "MUR": "Mauritius Rupee",
        "MVR": "Maldives (Maldive Islands) Rufiyaa", "MWK": "Malawi Kwacha", "MXN": "Mexico Peso",
        "MYR": "Malaysia Ringgit", "MZN": "Mozambique Metical", "NAD": "Namibia Dollar",
        "NGN": "Nigeria Naira", "NIO": "Nicaragua Cordoba", "NOK:": "Norway Krone", "NPR": "Nepal Rupee",
        "NZD": "New Zealand Dollar", "OMR": "Oman Rial", "PAB": "Panama Balboa", "PEN": "Peru Sol",
        "PGK": "Papua New Guinea Kina", "PHP": "Philippines Peso", "PKR": "Pakistan Rupee",
        "PLN": "Poland Zloty", "PYG": "Paraguay Guarani", "QAR": "Qatar Riyal", "RON": "Romania New Leu",
        "RSD": "Serbia Dinar", "RUB": "Russia Ruble", "RWF": "Rwanda Franc", "SAR": "Saudi Arabia Riyal",
        "SBD": "Solomon Islands Dollar", "SCR": "Seychelles Rupee", "SDG": "Sudan Pound",
        "SEK": "Sweden Krona", "SGD": "Singapore Dollar", "SHP": "Saint Helena Pound",
        "SLL": "Sierra Leone Leone", "SOS": "Somalia Shilling", "SPL:": "Seborga Luigino",
        "SR:D": "Suriname Dollar", "STD": "São Tomé and Príncipe Dobra", "SVC": "El Salvador Colon",
        "SYP": "Syria Pound", "SZL": "Swaziland Lilangeni", "THB": "Thailand Baht",
        "TJS": "Tajikistan Somoni", "TMT": "Turkmenistan Manat", "TND": "Tunisia Dinar",
        "TOP": "Tonga Pa'anga", "TRY": "Turkey Lira", "TTD": "Trinidad and Tobago Dollar",
        "TVD": "Tuvalu Dollar", "TWD": "Taiwan New Dollar", "TZS": "Tanzania Shilling",
        "UAH": "Ukraine Hryvnia", "UGX": "Uganda Shilling", "USD": "&#36;",
        "UYU": "Uruguay Peso", "UZS": "Uzbekistan Som", "VEF": "Venezuela Bolivar",
        "VND": "Viet Nam Dong", "VUV": "Vanuatu Vatu", "WST": "Samoa Tala",
        "XAF": "Communauté Financière Africaine (BEAC) CFA Franc BEAC", "XCD": "East Caribbean Dollar",
        "XDR": "International Monetary Fund (IMF) Special Drawing Rights",
        "XOF": "Communauté Financière Africaine (BCEAO) Franc",
        "XPF": "Comptoirs Français du Pacifique (CFP) Franc", "YER": "Yemen Rial",
        "ZAR": "South Africa Rand", "ZMW": "Zambia Kwacha", "ZWD": "Zimbabwe Dollar"
    };

    return currency_symbols[currency_symbol];
}

class RenderPieChart {
    constructor(data, id) {
        this.data = data;
        this.id = id;
    }

    shortages() {
        //console.log(data);

        var width = 300;
        var height = 300;
        var radius = 150;
        var colors = d3.scale.ordinal().range(['#259286', '#2176C7', '#FCF4DC', 'white', '#819090', '#A57706', '#EAE3CB', '#2e004d']);

        var pieData = unpack.pie(this.data);
        //console.log(pieData);

        var pie = d3.layout.pie().value(function (d) {
            //console.log(d[1]);
            return d[1];
        });

        var arc = d3.svg.arc().outerRadius(radius);

        var myChart = d3.select(this.id).append('svg').attr('width', width).attr('height', height).append('g').attr('transform', 'translate(' + (width - radius) + ',' + (height - radius) + ')').selectAll('path').data(pie(pieData)).enter().append('g').attr('class', 'slice');

        var slices = d3.selectAll('g.slice').append('path').attr('fill', function (d, i) {
            return colors(i);
        }).attr('opacity', .6).attr('d', arc);

        var text = d3.selectAll('g.slice').append('text').text(function (d, i) {
            //console.log(d.data[0]);

            return d.data[0];
        }).attr('text-anchor', 'middle').attr('fill', 'white').attr('transform', function (d) {
            d.innerRadius = 0;
            d.outerRadius = radius;
            return 'translate(' + arc.centroid(d) + ')';
        });
    }

    excess() {
        //console.log(data);

        var width = 300;
        var height = 300;
        var radius = 150;
        var colors = d3.scale.ordinal().range(['#259286', '#2176C7', '#FCF4DC', 'white', '#819090', '#A57706', '#EAE3CB', '#2e004d']);

        var pieData = unpack.excess(this.data, 'chart');
        //console.log(pieData);

        var pie = d3.layout.pie().value(function (d) {
            //console.log(d[1]);
            return d[1];
        });

        var arc = d3.svg.arc().outerRadius(radius);

        var myChart = d3.select(this.id).append('svg').attr('width', width).attr('height', height).append('g').attr('transform', 'translate(' + (width - radius) + ',' + (height - radius) + ')').selectAll('path').data(pie(pieData)).enter().append('g').attr('class', 'slice');

        var slices = d3.selectAll('g.slice').append('path').attr('fill', function (d, i) {
            return colors(i);
        }).attr('opacity', .6).attr('d', arc);

        var text = d3.selectAll('g.slice').append('text').text(function (d, i) {
            //console.log(d.data);

            return d.data[0];
        }).attr('text-anchor', 'middle').attr('fill', 'white').attr('transform', function (d) {
            d.innerRadius = 0;
            d.outerRadius = radius;
            return 'translate(' + arc.centroid(d) + ')';
        });
    }

    classification(id) {
        var width = 300;
        var height = 300;
        var radius = 150;
        var colors = d3.scale.ordinal().range(['#259286', '#2176C7', '#FCF4DC', 'white', '#819090', '#A57706', '#EAE3CB', '#2e004d']);

        var pieData = unpack.classification(this.data, id);
        //console.log(pieData);

        var pie = new d3.layout.pie().value(function (d) {
            //console.log(d[1]);
            return d[1];
        });

        var arc = new d3.svg.arc().outerRadius(radius);

        var myChart = d3.select(this.id).append('svg').attr('width', width).attr('height', height).append('g').attr('transform', 'translate(' + (width - radius) + ',' + (height - radius) + ')').selectAll('path').data(pie(pieData)).enter().append('g').attr('class', 'slice');

        var slices = d3.selectAll('g.slice').append('path').attr('fill', function (d, i) {
            return colors(i);
        }).attr('opacity', .6).attr('d', arc);

        var text = d3.selectAll('g.slice').append('text').text(function (d, i) {
            //console.log(d.data[0]);

            return d.data[0];
        }).attr('text-anchor', 'middle').attr('fill', 'white').attr('transform', function (d) {
            d.innerRadius = 0;
            d.outerRadius = radius;
            return 'translate(' + arc.centroid(d) + ')';
        });
    }

}

class RenderForceChart {
    constructor(data, id) {
        this.data = data;
        this.id = id;
    }

    classification_force() {
        var w = 800,
            h = 400;

        var circleWidth = 5;

        var palette = {
            "lightgray": "#819090",
            "gray": "#708284",
            "mediumgray": "#536870",
            "darkgray": "#475B62",

            "darkblue": "#0A2933",
            "darkerblue": "#042029",

            "paleryellow": "#FCF4DC",
            "paleyellow": "#EAE3CB",
            "yellow": "#A57706",
            "orange": "#BD3613",
            "red": "#D11C24",
            "pink": "#C61C6F",
            "purple": "#595AB7",
            "blue": "#2176C7",
            "green": "#259286",
            "yellowgreen": "#738A05"
        };

        var nodes1 = [];
        for (var s = 0; s < this.data.objects.length; s++) {
            if (s == 0) {
                nodes1.push({ name: this.data.objects[s].abc_xyz_classification });
            } else {
                nodes1.push({ name: this.data.objects[s].sku.sku_id, target: [0] });
            }
        }

        var nodes = [{ name: "Parent" }, { name: "child1" }, { name: "child2", target: [0] }, { name: "child3", target: [0] }, { name: "child4", target: [1] }, { name: "child5", target: [0, 1, 2, 3] }];

        var links = [];

        for (var i = 0; i < nodes1.length; i++) {
            if (nodes1[i].target !== undefined) {
                for (var x = 0; x < nodes1[i].target.length; x++) {
                    links.push({
                        source: nodes1[i],
                        target: nodes1[nodes1[i].target[x]]
                    });
                }
            }
        }

        var myChart = d3.select(this.id).append('svg').attr('width', w).attr('height', h);

        var force = d3.layout.force().nodes(nodes1).links([]).gravity(0.3).charge(-1000).size([w, h]);

        var link = myChart.selectAll('line').data(links).enter().append('line').attr('stroke', palette.gray);

        var node = myChart.selectAll('circle').data(nodes1).enter().append('g').call(force.drag);

        node.append('circle').attr('cx', function (d) {
            return d.x;
        }).attr('cy', function (d) {
            return d.y;
        }).attr('r', circleWidth).attr('fill', function (d, i) {
            if (i > 0) {
                return palette.blue;
            } else {
                return palette.pink;
            }
        });

        node.append('text').text(function (d) {
            return d.name;
        }).attr('fill', function (d, i) {
            if (i > 0) {
                return palette.paleyellow;
            } else {
                return palette.blue;
            }
        }).attr('x', function (d, i) {
            if (i > 0) {
                return circleWidth + 3;
            } else {
                return circleWidth - 5;
            }
        }).attr('y', function (d, i) {
            if (i > 0) {
                return circleWidth;
            } else {
                return circleWidth - 8;
            }
        }).attr('font-family', 'Roboto Slab').attr('text-anchor', function (d, i) {
            if (i > 0) {
                return 'beginning';
            } else {
                return 'end';
            }
        }).attr('font-size', function (d, i) {
            if (i > 0) {
                return '1em';
            } else {
                return '1.5em';
            }
        });

        force.on('tick', function (e) {
            node.attr('transform', function (d, i) {
                return 'translate(' + d.x + ', ' + d.y + ')';
            });

            link.attr('x1', function (d) {
                return d.source.x;
            }).attr('y1', function (d) {
                return d.source.y;
            }).attr('x2', function (d) {
                return d.target.x;
            }).attr('y2', function (d) {
                return d.target.y;
            });
        });

        force.start();
    }
}

function create_shortages_table(data) {
    var total_shortage = 0;
    //console.log(data.objects);
    //var max_shortage = Math.max(data.shortage_cost);
    //console.log(currency_symbol_allocator("AFN"));

    $("#shortage-table").append().html("<tr id='first'><th>SKU</th><th>Quantity on Hand</th><th>Average Orders</th>" + "<th>Shortage</th><th>Shortage Cost</th><th>Safety Stock</th><th>Reorder Level</th> " + "<th>Percentage Contribution</th><th>Revenue Rank</th><th>Classification</th></tr>");
    var percentage_stockoout = 0;
    var t = [];
    var largest = 0;
    var understocked_qoh = 0;
    var understocked_sku;
    var understocked_rol;
    var understocked_id;
    for (var i = 0; i < data.json_list.length; i++) {
        console.log(data.json_list[i].shortage_cost);
        total_shortage += data.json_list[i].shortage_cost;
        var shortage_sku_id;
        var shortage_units;
        var shortage_id;
        if (parseInt(data.json_list[i].shortage_cost) > parseInt(largest)) {
            largest = data.json_list[i].shortage_cost;
            //console.log(parseInt(largest));
            shortage_id = data.json_list[i].sku.id;
            shortage_sku_id = data.json_list[i].sku.sku_id;
            shortage_units = data.json_list[i].shortages;
        }

        if (parseInt(data.json_list[i].quantity_on_hand) < parseInt(data.json_list[i].safety_stock) / 2) {
            percentage_stockoout += 1;
        }
        var temp_net_stock = data.json_list[i].quantity_on_hand - data.json_list[i].reorder_level;
        if (Math.abs(temp_net_stock) > understocked_qoh) {
            understocked_qoh = data.json_list[i].quantity_on_hand;
            understocked_sku = data.json_list[i].sku.sku_id;
            understocked_rol = data.json_list[i].reorder_level;
            understocked_id = data.json_list[i].sku.id;
        }
    }

    // Percentage of top 10 SKU likely to face a stock-out situation. SKU is at risk below 50% of the safety stock.
    //This should be moved into the main library.
    percentage_stockoout = parseInt(percentage_stockoout) / data.json_list.length * 100;

    //Total Shortage of the to ten.
    //console.log(percentage_stockoout);
    $("#total-shortage").append().html("<h1><strong>" + format_number(total_shortage) + "</strong></h1>").find("> h1").css("color", "white");

    // top shortage SKU id
    $("#lg-shortage-sku").append().html("<a href=\"sku_detail/" + shortage_id + "\">" + "<strong>" + shortage_sku_id + "</strong></a>").find("> h1").css("color", "#2176C7");

    //largest shortage cost
    $("#lg-shortage-cost").append().html("<h1 class='slate-text-lg'><strong>" + format_number(largest) + "</strong></h1>").find("> h1").css("color", "white");

    //units for largest shortage cost.
    $("#lg-shortage-units").append().html("<h1><strong>" + format_number(shortage_units) + " units" + "</strong></h1>").find("> h1").css("color", "#819090");

    //percentage of SKUs likely to experience stock-out
    $("#shortage-percentage").append().html("<h1><strong>" + percentage_stockoout + "%" + "</strong></h1>").find("> h1").css("color", "#819090");

    $("#understocked-sku").append().html("<a href=\"sku_detail/" + understocked_id + "\">" + "<strong>" + understocked_sku + "</strong></a>").find("> h1").css("color", "#2176C7");

    $("#understocked-qoh").append().html("<h1><strong>" + "qty on hand: " + understocked_qoh + " units" + "</strong></h1>").find("> h1").css("color", "#819090");

    $("#understocked_rol").append().html("<h1><strong>" + "reorder level: " + understocked_rol + " units" + "</strong></h1>").find("> h1").css("color", "#819090");
}

function create_excess_table(data) {
    var total_excess = 0,
        percentage_excess = 0;

    $("#excess-table").append().html("<tr id='first'><th>SKU</th><th>Quantity on Hand</th><th>Average Orders</th>" + "<th>Excess</th><th>Excess Cost</th><th>Excess Inventory %</th><th>Safety Stock</th><th>Reorder Level</th><th>Classification</th></tr>");
    //console.log(excess_data);
    var obj;
    var largest = 0;
    var excess_sku_id;
    var excess_units;
    var excess_cost;
    var holding_cost = 0;
    var excess_id;

    for (var i = 0; i < data.objects.length; i++) {
        //console.log(excess_data[obj].sku_id);
        total_excess += data.objects[i].excess_cost;
        holding_cost += data.objects[i].quantity_on_hand * (data.objects[i].unit_cost * 0.25); //change later to be chosen by use
        var symbols = currency_symbol_allocator(data.objects[i].currency.currency_code);
        percentage_excess = Math.round(data.objects[i].excess_stock / data.objects[i].quantity_on_hand * 100);
        $("<tr><td><a href=\"sku_detail/" + data.objects[i].sku_id + "\">" + data.objects[i].sku.sku_id + "</td>" + "<td>" + format_number(data.objects[i].quantity_on_hand) + "</td>" + "<td>" + format_number(data.objects[i].average_orders) + "</td>" + "<td>" + format_number(data.objects[i].excess_stock) + "</td>" + "<td>" + currency_symbol_allocator(data.objects[i].currency.currency_code) + format_number(data.objects[i].excess_cost) + "</td>" + "<td>" + percentage_excess + "%" + "</td>" + "<td>" + format_number(data.objects[i].safety_stock) + "</td>" + "<td>" + format_number(data.objects[i].reorder_level) + "</td>" + "<td><a href=\"abcxyz/" + data.objects[i].abc_xyz_classification + "\">" + data.objects[i].abc_xyz_classification + "</a></td></tr>").insertAfter("#excess-table tr:last");

        if (parseInt(data.objects[i].excess_cost) > parseInt(largest)) {
            largest = data.objects[i].excess_cost;
            //console.log(parseInt(largest));
            excess_sku_id = data.objects[i].sku.sku_id;
            excess_units = data.objects[i].excess_stock;
            excess_cost = data.objects[i].excess_cost;
            excess_id = data.objects[i].sku.id;
        }
    }

    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: '/api/total_inventory',
        dataType: 'json',
        async: true,
        data: "{}",
        success: function (data) {
            // console.log(data);
            var items = [...data.json_list];
            //console.log(items.length);
            var total_invetory = 0;
            for (i = 0; i < items.length; i++) {

                total_invetory += items[i].quantity_on_hand * items[i].unit_cost;

                //console.log(total_invetory);
            }
            var percentage_excess;
            //console.log(total_invetory);
            percentage_excess = Math.round(total_excess / total_invetory * 100, 0);

            $("#excess-inventory-sl").append().html("<h1><strong>" + percentage_excess + "%" + "</strong></h1>").find("> h1").css("color", "#D11C29");
        },
        error: function (result) {}
    });

    // top excess pebble
    $("#lg-excess-sku").append().html("<a href=\"sku_detail/" + excess_id + "\">" + "<strong>" + excess_sku_id + "</strong></a>").find("> h1").css("color", "#2176C7");
    $("#lg-excess-cost").append().html("<h1 class='slate-text-lg'><strong>" + symbols + format_number(excess_cost) + "</strong></h1>").find("> h1").css("color", "white");
    $("#lg-excess-units").append().html("<h1><strong>" + format_number(excess_units) + " units" + "</strong></h1>").find("> h1").css("color", "#819090");
    $("#total-excess").append().html("<h1 class='slate-text-lg'><strong>" + symbols + format_number(total_excess) + "</strong></h1>").find("> h1").css("color", "white");

    $("#excess-holding-cost-sl").append().html("<h1 class='slate-text-lg'><strong>" + symbols + format_number(holding_cost) + "</strong></h1>").find("> h1").css("color", "white");
}

function create_classification_table(data) {

    var abc_xyz_data = new unpack.abc_xyz(data, 'table');
    var currency_code;
    //console.log(abc_xyz_data);

    $("#classification-table").append().html("<tr id='classification-row'><th>Classification</th><th>Revenue</th><th>Shortages</th>" + "<th>Excess</th></tr>");
    //console.log(excess_data);

    var obj;

    var symbols = currency_symbol_allocator(abc_xyz_data[0].currency_code);
    //console.log(symbols, abc_xyz_data[0].currency_code);
    for (obj in abc_xyz_data) {
        //console.log(abc_xyz_data[obj].abc_xyz_classification);
        $("<tr><td><a href=\"abcxyz/" + abc_xyz_data[obj].abc_xyz_classification + "\">" + abc_xyz_data[obj].abc_xyz_classification + "</a>" + "<td>" + symbols + format_number(abc_xyz_data[obj].total_revenue) + "</td>" + "<td>" + symbols + format_number(abc_xyz_data[obj].total_shortages) + "</td>" + "<td>" + symbols + format_number(abc_xyz_data[obj].total_excess) + "</td>" + "</td></tr>").insertAfter("#classification-table tr:last");
    }

    var max_shortage = 0;
    var max_class;
    var max_excess = 0;
    var excess_class;
    var total_shortages = 0;
    var total_excess = 0;
    var item;
    var tempValue;
    var tempClass;
    for (item in abc_xyz_data) {
        if (abc_xyz_data[item].total_shortages > max_shortage) {
            max_shortage = abc_xyz_data[item].total_shortages;
            max_class = abc_xyz_data[item].abc_xyz_classification;
        }
        if (abc_xyz_data[item].total_excess > max_excess) {
            max_excess = abc_xyz_data[item].total_excess;
            excess_class = abc_xyz_data[item].abc_xyz_classification;
        }
        total_shortages += abc_xyz_data[item].total_shortages;
        total_excess += abc_xyz_data[item].total_excess;
    }

    $("#lg-shortage-classification").append().html("<h1 class='slate-text-lg'><strong>" + symbols + format_number(max_shortage) + "</strong></h1>").find("> h1").css("color", "white");
    $("#lg-shortage-classification-class").append().html("<a href=\"abcxyz/" + max_class + "\">" + "<strong>" + max_class + "</strong></a>").find("> h1").css("color", "#2176C7");
    $("#lg-total-shortage").append().html("<h1 class='slate-text-lg'><strong>" + symbols + format_number(total_shortages) + "</strong></h1>").find("> h1").css("color", "white");
    $("#lg-shortage-percentage").append().html("<h1><strong>" + Math.round(max_shortage / total_shortages * 100) + "% of Total Shortage" + "</strong></h1>").find("> h1").css("color", "#708284");

    $("#lg-excess-classification").append().html("<h1 class='slate-text-lg'><strong>" + symbols + format_number(max_excess) + "</strong></h1>").find("> h1").css("color", "white");
    $("#lg-excess-classification-class").append().html("<a href=\"abcxyz/" + excess_class + "\">" + "<strong>" + excess_class + "</strong>").find("> h1").css("color", "#2176C7");
    $("#lg-excess-percentage").append().html("<h1><strong>" + Math.round(max_excess / total_excess * 100) + "% of Total Excess" + "</strong></h1>").find("> h1").css("color", "#708284");
    $("#lg-total-excess").append().html("<h1 class='slate-text-lg'><strong>" + symbols + format_number(total_excess) + "</strong></h1>").find("> h1").css("color", "white");
}

// --------------Graphing-----------------------

// change functions to graph rendering class
/*function render_revenue_graph(data, id) {
 var barData = unpack.sku_detail(data, "revenue");//change to enums
 var tempData = [];

 //console.log(barData);
 //var height = 350,
 //   width = 300,
 var margin = {top: 30, right: 20, bottom: 40, left: 90};

 var height = 350 - margin.top - margin.bottom;
 var width = 400 - margin.left - margin.right;
 var barWidth = 10;
 var barOffset = 5;

 var tempColor;


 var yScale = d3.scale.linear()
 .domain([0, d3.max(barData)]) //  calculates the max range of the chart area
 .range([0, height]); // the range of the chart area

 var xScale = d3.scale.ordinal()
 .domain(d3.range(0, barData.length))
 .rangeBands([0, width]);

 var colors = d3.scale.linear()
 .domain([0, barData.length * .33, barData.length * .88, barData.length])
 .range(['#FFB832', '#C61C6F', '#C31C6F', '#382982']); //the number of values in the domain must match the number of values in the range

 var myChart = d3.select(id).append('svg')
 .style('background', 'transparent')
 .attr('width', width + margin.left + margin.right)
 .attr('height', height + margin.top + margin.bottom)
 .append('g')
 .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')
 .selectAll('rect').data(barData)
 .enter().append('rect') //the data command reads the bar data and the appends the selectall rect for each piece of data
 .style('fill', colors)
 .attr('width', xScale.rangeBand())
 .attr('height', 0)
 .attr('x', function (d, i) {
 return xScale(i);
 })
 .attr('y', height)
 .on('mouseover', function (d) {

 tooltip.transaction()
 .style('opacity', 0.5);
 tooltip.html(d)
 .style('left', (d3.event.pageX - 35) + 'px')
 .style('top', (d3.event.pageY - 30) + 'px');

 tempColor = this.style.fill;

 d3.select(this)
 .style('opacity', .5)
 .style('fill', '#389334')

 }).on('mouseout', function (d) {
 d3.select(this)
 .style('opacity', 1)
 .style('fill', tempColor)
 });

 myChart.transition()
 .attr('height', function (d) {
 return yScale(d);
 })
 .attr('y', function (d) {
 return height - yScale(d);
 })
 .delay(function (d, i) {
 return i * 20;
 })
 .duration(1000)
 .ease('elastic');


 var tooltip = d3.select('body')
 .append('div')
 .style('position', 'absolute')
 .style('background', 'white')
 .style('padding', '0 10px')
 .style('opacity', 0);

 var vGuideScale = d3.scale.linear()
 .domain([0, d3.max(barData)]).range([height, 0]); //reversing the order of the scale on the y axis
 var vAxis = d3.svg.axis()
 .scale(vGuideScale)
 .orient('left')
 .ticks(10);

 var vGuide = d3.select('svg').append('g');
 vAxis(vGuide);
 vGuide.attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');
 vGuide.selectAll('path')
 .style({fill: 'none', stroke: "#000"});
 vGuide.selectAll('line')
 .style({stroke: "#000"});

 var hAxis = d3.svg.axis()
 .scale(xScale)
 .orient('bottom')
 .tickValues(xScale.domain().filter(function (d, i) {
 return !(i % (barData.length / 10));
 }));

 var hGuide = d3.select('svg').append('g');
 hAxis(hGuide);
 hGuide.attr('transform', 'translate(' + margin.left + ', ' + (height + margin.top) + ')');
 hGuide.selectAll('path')
 .style({fill: 'none', stroke: "#000"});
 hGuide.selectAll('line')
 .style({stroke: "#000"});


 }
 */

function render_shortages_chart(data, id) {
    var bardata = unpack.shortages(data, 'chart');
    var nums = [];
    var switchColor;

    for (i in bardata) {
        nums.push(bardata[i][1]);
    }

    var tooltip = d3.select('body').append('div').style('position', 'absolute').style('background', 'white').style('padding', '0 10px').style('opacity', 0);

    //console.log(nums);

    var margin = { top: 30, right: 50, bottom: 40, left: 95 };

    var height = 350 - margin.top - margin.bottom;
    var width = 600 - margin.left - margin.right;

    var colors = d3.scale.linear().domain([0, nums.length * .33, nums.length * .66, nums.length]).range(['white', '#259286', '#738A05', '#2176C7']);

    var yScale = d3.scale.linear().domain([0, d3.max(nums)]).range([0, height]);

    var xScale = d3.scale.ordinal().domain(d3.range(0, nums.length)).rangeBands([0, width], .2); // space the bars on the chart

    var shortage_chart = d3.select(id).append('svg').style('background', '#0A2933;').attr('width', width + margin.left + margin.right).attr('height', height + margin.top + margin.bottom).append('g').attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')') //moving the chart graphic
    .selectAll('rect').data(nums).enter().append('rect').style('fill', function (d, i) {
        return colors(i);
    }).attr('width', xScale.rangeBand()).attr('height', 0).attr('x', function (d, i) {
        return xScale(i);
    }).attr('y', height).on('mouseover', function (d) {
        //console.log(d);
        tooltip.transition().style('opacity', 0.5);
        tooltip.html(d).style('left', d3.event.pageX - 35 + 'px').style('top', d3.event.pageY - 30 + 'px');

        switchColor = this.style.fill;
        d3.select(this).style('opacity', .5);
        d3.select(this).style('fill', '#D11C24');
    }).on('mouseout', function (d) {
        d3.select(this).transition().delay(300).duration(300).style('fill', switchColor);
        d3.select(this).style('opacity', 1);
    });
    //transitions graph in
    shortage_chart.transition().attr('height', function (d, i) {
        return yScale(d);
    }).attr('y', function (d) {
        return height - yScale(d);
    }).delay(function (d, i) {
        return i * 70;
    }).ease('elastic');

    var vGuideScale = d3.scale.linear().domain([0, d3.max(nums)]).range([height, 0]); //reversing the order of the scale on the y axi

    var vAxis = d3.svg.axis().scale(vGuideScale).orient('left').ticks(10);

    var vGuide = d3.select('#shortage-chart > svg').append('g');
    vAxis(vGuide);
    vGuide.attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');
    vGuide.selectAll('path').style({ fill: 'none', stroke: "white" });
    vGuide.selectAll('line').style({ stroke: "white" });
    vGuide.selectAll('text').style({ stroke: "grey" });

    var name = d3.scale.ordinal().range(['#259286', '#2176C7', '#FCF4DC', 'white', '#819090', '#A57706', '#EAE3CB', '#2e004d']);

    var hAxis = d3.svg.axis().scale(xScale).orient('bottom').tickValues(xScale.domain().filter(function (d, i) {
        return !(i % (nums.length / 5));
    }));

    var hGuide = d3.select('#shortage-chart > svg').append('g');
    hAxis(hGuide);
    hGuide.attr('transform', 'translate(' + margin.left + ', ' + (height + margin.top) + ')');
    hGuide.selectAll('path').style({ fill: 'none', stroke: "white" });
    hGuide.selectAll('line').style({ stroke: "white" });
    hGuide.selectAll('text').style({ stroke: "grey" });
}

function render_excess_chart(data, id) {
    var bardata = unpack.excess_cost(data, 'chart');
    //console.log(bardata);
    var nums = [];
    var switchColor;

    for (i in bardata) {
        nums.push(bardata[i][1]);
    }

    var tooltip = d3.select('body').append('div').style('position', 'absolute').style('background', 'white').style('padding', '0 10px').style('opacity', 0);

    //console.log(nums);

    var margin = { top: 30, right: 50, bottom: 40, left: 95 };

    var height = 350 - margin.top - margin.bottom;
    var width = 600 - margin.left - margin.right;

    var colors = d3.scale.linear().domain([0, nums.length * .33, nums.length * .66, nums.length]).range(['white', '#259286', '#738A05', '#2176C7']);

    var yScale = d3.scale.linear().domain([0, d3.max(nums)]).range([0, height]);

    var xScale = d3.scale.ordinal().domain(d3.range(0, nums.length)).rangeBands([0, width], .2); // space the bars on the chart

    var shortage_chart = d3.select(id).append('svg').style('background', '#0A2933;').attr('width', width + margin.left + margin.right).attr('height', height + margin.top + margin.bottom).append('g').attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')') //moving the chart graphic
    .selectAll('rect').data(nums).enter().append('rect').style('fill', function (d, i) {
        return colors(i);
    }).attr('width', xScale.rangeBand()).attr('height', 0).attr('x', function (d, i) {
        return xScale(i);
    }).attr('y', height).on('mouseover', function (d) {
        //console.log(d);
        tooltip.transition().style('opacity', 0.5);
        tooltip.html(d).style('left', d3.event.pageX - 35 + 'px').style('top', d3.event.pageY - 30 + 'px');

        switchColor = this.style.fill;
        d3.select(this).style('opacity', .5);
        d3.select(this).style('fill', '#D11C24');
    }).on('mouseout', function (d) {
        d3.select(this).transition().delay(300).duration(300).style('fill', switchColor);
        d3.select(this).style('opacity', 1);
    });
    //transitions graph in
    shortage_chart.transition().attr('height', function (d, i) {
        return yScale(d);
    }).attr('y', function (d) {
        return height - yScale(d);
    }).delay(function (d, i) {
        return i * 70;
    }).ease('elastic');

    var vGuideScale = d3.scale.linear().domain([0, d3.max(nums)]).range([height, 0]); //reversing the order of the scale on the y axi

    var vAxis = d3.svg.axis().scale(vGuideScale).orient('left').ticks(10);

    var vGuide = d3.select('#excess-chart > svg').append('g');
    vAxis(vGuide);
    vGuide.attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');
    vGuide.selectAll('path').style({ fill: 'none', stroke: "white" });
    vGuide.selectAll('line').style({ stroke: "white" });
    vGuide.selectAll('text').style({ stroke: "grey" });

    var name = d3.scale.ordinal().range(['#259286', '#2176C7', '#FCF4DC', 'white', '#819090', '#A57706', '#EAE3CB', '#2e004d']);

    var hAxis = d3.svg.axis().scale(xScale).orient('bottom').tickValues(xScale.domain().filter(function (d, i) {
        return !(i % (nums.length / 5));
    }));

    var hGuide = d3.select('#excess-chart > svg').append('g');
    hAxis(hGuide);
    hGuide.attr('transform', 'translate(' + margin.left + ', ' + (height + margin.top) + ')');
    hGuide.selectAll('path').style({ fill: 'none', stroke: "white" });
    hGuide.selectAll('line').style({ stroke: "white" });
    hGuide.selectAll('text').style({ stroke: "grey" });
}

//# sourceMappingURL=auxiliary-compiled.js.map

//# sourceMappingURL=auxiliary-compiled-compiled.js.map