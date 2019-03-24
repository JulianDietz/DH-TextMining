$(document).ready(function () {
    $(".toggle_button").click(function () {

        let $this = $(this);
        let collapseEl = $($this.attr("data-collapse"));

        let statisticDisplayType = $this.attr("data-statisticdisplaytype");


        if ($this.attr("data-ready") == "false") {
            setTimeout(function () {
                console.log(statisticDisplayType)
                switch (statisticDisplayType) {

                    case "numeric-total":
                        returnGraphNumericTotal($this.attr("id"), collapseEl, null);
                        break;
                    case "numeric-section":
                        returnGraphNumericSection($this.attr("id"), collapseEl, null)
                        break;
                    case "text-total":

                        break;
                    case "text-section":
                        break;
                }
                $this.toggleClass("toggle_button_closed").toggleClass("toggle_button_open");
                collapseEl.collapse('toggle');
                $this.attr("data-ready", "true");
                $this.next().children(".indicator").attr("src", "/static/img/results/verified.png")

            }, 0);

            $this.next().children(".indicator").attr("src", "/static/img/results/stopwatch.png")


        } else {
            $(collapseEl).collapse('toggle');
            $this.toggleClass("toggle_button_closed").toggleClass("toggle_button_open");
        }
    });

    $(".collapse").on('show.bs.collapse', function () {
        console.log("opening");
    });

    $(".collapse").on('hide.bs.collapse', function () {
        console.log("hidden");
    });
});


response.AutorCount.Stat.key
response.AutorCount.RawData

function returnGraphNumericTotal(IDMetricEl, htmlEl, data2) {
    //TODO debug v
    let sumstat = [
        {"key": "Korpus 1", "value": {"q1": 4.8, "median": 5, "q3": 5.2, "interQuantileRange": 0.40000000000000036, "min": 4.199999999999999, "max": 5.800000000000001}},
        {"key": "Korpus 2", "value": {"q1": 5.6, "median": 5.9, "q3": 6.3, "interQuantileRange": 0.7000000000000002, "min": 4.549999999999999, "max": 7.35}}]

    let rawData = JSON.parse('[{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"4.9","corpus":"Korpus 2"},{"metric_value":"4.7","corpus":"Korpus 2"},{"metric_value":"4.6","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"5.4","corpus":"Korpus 2"},{"metric_value":"4.6","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"4.4","corpus":"Korpus 2"},{"metric_value":"4.9","corpus":"Korpus 2"},{"metric_value":"5.4","corpus":"Korpus 2"},{"metric_value":"4.8","corpus":"Korpus 2"},{"metric_value":"4.8","corpus":"Korpus 2"},{"metric_value":"4.3","corpus":"Korpus 2"},{"metric_value":"5.8","corpus":"Korpus 2"},{"metric_value":"5.7","corpus":"Korpus 2"},{"metric_value":"5.4","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"5.7","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"5.4","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"4.6","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"4.8","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"5.2","corpus":"Korpus 2"},{"metric_value":"5.2","corpus":"Korpus 2"},{"metric_value":"4.7","corpus":"Korpus 2"},{"metric_value":"4.8","corpus":"Korpus 2"},{"metric_value":"5.4","corpus":"Korpus 2"},{"metric_value":"5.2","corpus":"Korpus 2"},{"metric_value":"5.5","corpus":"Korpus 2"},{"metric_value":"4.9","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"5.5","corpus":"Korpus 2"},{"metric_value":"4.9","corpus":"Korpus 2"},{"metric_value":"4.4","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"4.5","corpus":"Korpus 2"},{"metric_value":"4.4","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"4.8","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"4.6","corpus":"Korpus 2"},{"metric_value":"5.3","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"7","corpus":"Korpus 1"},{"metric_value":"6.4","corpus":"Korpus 1"},{"metric_value":"6.9","corpus":"Korpus 1"},{"metric_value":"5.5","corpus":"Korpus 1"},{"metric_value":"6.5","corpus":"Korpus 1"},{"metric_value":"5.7","corpus":"Korpus 1"},{"metric_value":"6.3","corpus":"Korpus 1"},{"metric_value":"4.9","corpus":"Korpus 1"},{"metric_value":"6.6","corpus":"Korpus 1"},{"metric_value":"5.2","corpus":"Korpus 1"},{"metric_value":"5","corpus":"Korpus 1"},{"metric_value":"5.9","corpus":"Korpus 1"},{"metric_value":"6","corpus":"Korpus 1"},{"metric_value":"6.1","corpus":"Korpus 1"},{"metric_value":"5.6","corpus":"Korpus 1"},{"metric_value":"6.7","corpus":"Korpus 1"},{"metric_value":"5.6","corpus":"Korpus 1"},{"metric_value":"5.8","corpus":"Korpus 1"},{"metric_value":"6.2","corpus":"Korpus 1"},{"metric_value":"5.6","corpus":"Korpus 1"},{"metric_value":"5.9","corpus":"Korpus 1"},{"metric_value":"6.1","corpus":"Korpus 1"},{"metric_value":"6.3","corpus":"Korpus 1"},{"metric_value":"6.1","corpus":"Korpus 1"},{"metric_value":"6.4","corpus":"Korpus 1"},{"metric_value":"6.6","corpus":"Korpus 1"},{"metric_value":"6.8","corpus":"Korpus 1"},{"metric_value":"6.7","corpus":"Korpus 1"},{"metric_value":"6","corpus":"Korpus 1"},{"metric_value":"5.7","corpus":"Korpus 1"},{"metric_value":"5.5","corpus":"Korpus 1"},{"metric_value":"5.5","corpus":"Korpus 1"},{"metric_value":"5.8","corpus":"Korpus 1"},{"metric_value":"6","corpus":"Korpus 1"},{"metric_value":"5.4","corpus":"Korpus 1"},{"metric_value":"6","corpus":"Korpus 1"},{"metric_value":"6.7","corpus":"Korpus 1"},{"metric_value":"6.3","corpus":"Korpus 1"},{"metric_value":"5.6","corpus":"Korpus 1"},{"metric_value":"5.5","corpus":"Korpus 1"},{"metric_value":"5.5","corpus":"Korpus 1"},{"metric_value":"6.1","corpus":"Korpus 1"},{"metric_value":"5.8","corpus":"Korpus 1"},{"metric_value":"5","corpus":"Korpus 1"},{"metric_value":"5.6","corpus":"Korpus 1"},{"metric_value":"5.7","corpus":"Korpus 1"},{"metric_value":"5.7","corpus":"Korpus 1"},{"metric_value":"6.2","corpus":"Korpus 1"},{"metric_value":"5.1","corpus":"Korpus 1"},{"metric_value":"5.7","corpus":"Korpus 1"}]');
    let rawData2 = JSON.parse('[{"metric_value":"5.1","corpus":"Korpus 1"},{"metric_value":"4.9","corpus":"Korpus 1"},{"metric_value":"4.7","corpus":"Korpus 1"},{"metric_value":"4.6","corpus":"Korpus 1"},{"metric_value":"5","corpus":"Korpus 1"},{"metric_value":"5.4","corpus":"Korpus 1"},{"metric_value":"4.6","corpus":"Korpus 1"},{"metric_value":"5","corpus":"Korpus 1"},{"metric_value":"4.4","corpus":"Korpus 1"},{"metric_value":"4.9","corpus":"Korpus 1"},{"metric_value":"5.4","corpus":"Korpus 1"},{"metric_value":"4.8","corpus":"Korpus 1"},{"metric_value":"4.8","corpus":"Korpus 1"},{"metric_value":"4.3","corpus":"Korpus 1"},{"metric_value":"5.8","corpus":"Korpus 1"},{"metric_value":"5.7","corpus":"Korpus 1"},{"metric_value":"5.4","corpus":"Korpus 1"},{"metric_value":"5.1","corpus":"Korpus 1"},{"metric_value":"5.7","corpus":"Korpus 1"},{"metric_value":"5.1","corpus":"Korpus 1"},{"metric_value":"5.4","corpus":"Korpus 1"},{"metric_value":"5.1","corpus":"Korpus 1"},{"metric_value":"4.6","corpus":"Korpus 1"},{"metric_value":"5.1","corpus":"Korpus 1"},{"metric_value":"4.8","corpus":"Korpus 1"},{"metric_value":"5","corpus":"Korpus 1"},{"metric_value":"5","corpus":"Korpus 1"},{"metric_value":"5.2","corpus":"Korpus 1"},{"metric_value":"5.2","corpus":"Korpus 1"},{"metric_value":"4.7","corpus":"Korpus 1"},{"metric_value":"4.8","corpus":"Korpus 1"},{"metric_value":"5.4","corpus":"Korpus 1"},{"metric_value":"5.2","corpus":"Korpus 1"},{"metric_value":"5.5","corpus":"Korpus 1"},{"metric_value":"4.9","corpus":"Korpus 1"},{"metric_value":"5","corpus":"Korpus 1"},{"metric_value":"5.5","corpus":"Korpus 1"},{"metric_value":"4.9","corpus":"Korpus 1"},{"metric_value":"4.4","corpus":"Korpus 1"},{"metric_value":"5.1","corpus":"Korpus 1"},{"metric_value":"5","corpus":"Korpus 1"},{"metric_value":"4.5","corpus":"Korpus 1"},{"metric_value":"4.4","corpus":"Korpus 1"},{"metric_value":"5","corpus":"Korpus 1"},{"metric_value":"5.1","corpus":"Korpus 1"},{"metric_value":"4.8","corpus":"Korpus 1"},{"metric_value":"5.1","corpus":"Korpus 1"},{"metric_value":"4.6","corpus":"Korpus 1"},{"metric_value":"5.3","corpus":"Korpus 1"},{"metric_value":"5","corpus":"Korpus 1"},{"metric_value":"7","corpus":"Korpus 2"},{"metric_value":"6.4","corpus":"Korpus 2"},{"metric_value":"6.9","corpus":"Korpus 2"},{"metric_value":"5.5","corpus":"Korpus 2"},{"metric_value":"6.5","corpus":"Korpus 2"},{"metric_value":"5.7","corpus":"Korpus 2"},{"metric_value":"6.3","corpus":"Korpus 2"},{"metric_value":"4.9","corpus":"Korpus 2"},{"metric_value":"6.6","corpus":"Korpus 2"},{"metric_value":"5.2","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"5.9","corpus":"Korpus 2"},{"metric_value":"6","corpus":"Korpus 2"},{"metric_value":"6.1","corpus":"Korpus 2"},{"metric_value":"5.6","corpus":"Korpus 2"},{"metric_value":"6.7","corpus":"Korpus 2"},{"metric_value":"5.6","corpus":"Korpus 2"},{"metric_value":"5.8","corpus":"Korpus 2"},{"metric_value":"6.2","corpus":"Korpus 2"},{"metric_value":"5.6","corpus":"Korpus 2"},{"metric_value":"5.9","corpus":"Korpus 2"},{"metric_value":"6.1","corpus":"Korpus 2"},{"metric_value":"6.3","corpus":"Korpus 2"},{"metric_value":"6.1","corpus":"Korpus 2"},{"metric_value":"6.4","corpus":"Korpus 2"},{"metric_value":"6.6","corpus":"Korpus 2"},{"metric_value":"6.8","corpus":"Korpus 2"},{"metric_value":"6.7","corpus":"Korpus 2"},{"metric_value":"6","corpus":"Korpus 2"},{"metric_value":"5.7","corpus":"Korpus 2"},{"metric_value":"5.5","corpus":"Korpus 2"},{"metric_value":"5.5","corpus":"Korpus 2"},{"metric_value":"5.8","corpus":"Korpus 2"},{"metric_value":"6","corpus":"Korpus 2"},{"metric_value":"5.4","corpus":"Korpus 2"},{"metric_value":"6","corpus":"Korpus 2"},{"metric_value":"6.7","corpus":"Korpus 2"},{"metric_value":"6.3","corpus":"Korpus 2"},{"metric_value":"5.6","corpus":"Korpus 2"},{"metric_value":"5.5","corpus":"Korpus 2"},{"metric_value":"5.5","corpus":"Korpus 2"},{"metric_value":"6.1","corpus":"Korpus 2"},{"metric_value":"5.8","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"5.6","corpus":"Korpus 2"},{"metric_value":"5.7","corpus":"Korpus 2"},{"metric_value":"5.7","corpus":"Korpus 2"},{"metric_value":"6.2","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"5.7","corpus":"Korpus 2"}]');


    let statisticalData = sumstat;
    //TODO debug ^

    let metricContainer = d3.select(htmlEl[0]);

    let metricDescription = metricContainer.append("div").classed("metricDescription", true).classed("row", true);

    //Add a statistical overview for each corpus
    for (corpus of statisticalData) {
        console.log(corpus);

        let metricDescriptionCol = metricDescription.append("div").classed("col", true).attr("style", "display: inline-block;");
        metricDescriptionCol.append("div").classed("metricDescriptionColHeader", true).text(corpus.key);
        let metricDescriptionTags = metricDescriptionCol.append("div").classed("metricDescriptionColTags", true);

        //TODO keys abgleichen
        metricDescriptionTags.append("p").classed("metric-data modus-text", true).text(corpus.value.max.toFixed(2)).attr("data-before", "Modus: ");
        metricDescriptionTags.append("p").classed("metric-data median-text", true).text(corpus.value.median).attr("data-before", "Median: ");
        metricDescriptionTags.append("p").classed("metric-data average-text", true).text(corpus.value.q3).attr("data-before", "Durchschnitt: ");
        metricDescriptionTags.append("p").classed("metric-data variance-text", true).text(corpus.value.interQuantileRange.toFixed(2)).attr("data-before", "Varianz: ");
    }
    ;

    //drat the boxplot
    drawBoxplot(metricContainer, statisticalData, rawData);

    //Create CSV file and download
    createCSVdownload(IDMetricEl, rawData);
};

function returnGraphNumericSection(IDMetricEl, htmlEl, data2) {
    //TODO debug v
    let sumstat = [
        {"key": "Korpus 1", "value": {"q1": 4.8, "median": 5, "q3": 5.2, "interQuantileRange": 0.40000000000000036, "min": 4.199999999999999, "max": 5.800000000000001}},
        {"key": "Korpus 2", "value": {"q1": 5.6, "median": 5.9, "q3": 6.3, "interQuantileRange": 0.7000000000000002, "min": 4.549999999999999, "max": 7.35}}]

    let rawData = [{
        "section" : "h1","rawData": [{"metric_value": "5.1", "corpus": "Korpus 2"}, {"metric_value": "4.9", "corpus": "Korpus 2"}, {"metric_value": "4.7", "corpus": "Korpus 2"}, {
            "metric_value": "4.6",
            "corpus": "Korpus 2"
        }, {"metric_value": "5", "corpus": "Korpus 2"}, {"metric_value": "5.4", "corpus": "Korpus 2"}, {"metric_value": "4.6", "corpus": "Korpus 2"}, {
            "metric_value": "5",
            "corpus": "Korpus 2"
        }, {"metric_value": "4.4", "corpus": "Korpus 2"}, {"metric_value": "4.9", "corpus": "Korpus 2"}, {"metric_value": "5.4", "corpus": "Korpus 2"}, {
            "metric_value": "4.8",
            "corpus": "Korpus 2"
        }, {"metric_value": "4.8", "corpus": "Korpus 2"}, {"metric_value": "4.3", "corpus": "Korpus 2"}, {"metric_value": "5.8", "corpus": "Korpus 2"}, {
            "metric_value": "5.7",
            "corpus": "Korpus 2"
        }, {"metric_value": "5.4", "corpus": "Korpus 2"}, {"metric_value": "5.1", "corpus": "Korpus 2"}, {"metric_value": "5.7", "corpus": "Korpus 2"}, {
            "metric_value": "5.1",
            "corpus": "Korpus 2"
        }, {"metric_value": "5.4", "corpus": "Korpus 2"}, {"metric_value": "5.1", "corpus": "Korpus 2"}, {"metric_value": "4.6", "corpus": "Korpus 2"}, {
            "metric_value": "5.1",
            "corpus": "Korpus 2"
        }, {"metric_value": "4.8", "corpus": "Korpus 2"}, {"metric_value": "5", "corpus": "Korpus 2"}, {"metric_value": "5", "corpus": "Korpus 2"}, {
            "metric_value": "5.2",
            "corpus": "Korpus 2"
        }, {"metric_value": "5.2", "corpus": "Korpus 2"}, {"metric_value": "4.7", "corpus": "Korpus 2"}, {"metric_value": "4.8", "corpus": "Korpus 2"}, {
            "metric_value": "5.4",
            "corpus": "Korpus 2"
        }, {"metric_value": "5.2", "corpus": "Korpus 2"}, {"metric_value": "5.5", "corpus": "Korpus 2"}, {"metric_value": "4.9", "corpus": "Korpus 2"}, {
            "metric_value": "5",
            "corpus": "Korpus 2"
        }, {"metric_value": "5.5", "corpus": "Korpus 2"}, {"metric_value": "4.9", "corpus": "Korpus 2"}, {"metric_value": "4.4", "corpus": "Korpus 2"}, {
            "metric_value": "5.1",
            "corpus": "Korpus 2"
        }, {"metric_value": "5", "corpus": "Korpus 2"}, {"metric_value": "4.5", "corpus": "Korpus 2"}, {"metric_value": "4.4", "corpus": "Korpus 2"}, {
            "metric_value": "5",
            "corpus": "Korpus 2"
        }, {"metric_value": "5.1", "corpus": "Korpus 2"}, {"metric_value": "4.8", "corpus": "Korpus 2"}, {"metric_value": "5.1", "corpus": "Korpus 2"}, {
            "metric_value": "4.6",
            "corpus": "Korpus 2"
        }, {"metric_value": "5.3", "corpus": "Korpus 2"}, {"metric_value": "5", "corpus": "Korpus 2"}, {"metric_value": "7", "corpus": "Korpus 1"}, {
            "metric_value": "6.4",
            "corpus": "Korpus 1"
        }, {"metric_value": "6.9", "corpus": "Korpus 1"}, {"metric_value": "5.5", "corpus": "Korpus 1"}, {"metric_value": "6.5", "corpus": "Korpus 1"}, {
            "metric_value": "5.7",
            "corpus": "Korpus 1"
        }, {"metric_value": "6.3", "corpus": "Korpus 1"}, {"metric_value": "4.9", "corpus": "Korpus 1"}, {"metric_value": "6.6", "corpus": "Korpus 1"}, {
            "metric_value": "5.2",
            "corpus": "Korpus 1"
        }, {"metric_value": "5", "corpus": "Korpus 1"}, {"metric_value": "5.9", "corpus": "Korpus 1"}, {"metric_value": "6", "corpus": "Korpus 1"}, {
            "metric_value": "6.1",
            "corpus": "Korpus 1"
        }, {"metric_value": "5.6", "corpus": "Korpus 1"}, {"metric_value": "6.7", "corpus": "Korpus 1"}, {"metric_value": "5.6", "corpus": "Korpus 1"}, {
            "metric_value": "5.8",
            "corpus": "Korpus 1"
        }, {"metric_value": "6.2", "corpus": "Korpus 1"}, {"metric_value": "5.6", "corpus": "Korpus 1"}, {"metric_value": "5.9", "corpus": "Korpus 1"}, {
            "metric_value": "6.1",
            "corpus": "Korpus 1"
        }, {"metric_value": "6.3", "corpus": "Korpus 1"}, {"metric_value": "6.1", "corpus": "Korpus 1"}, {"metric_value": "6.4", "corpus": "Korpus 1"}, {
            "metric_value": "6.6",
            "corpus": "Korpus 1"
        }, {"metric_value": "6.8", "corpus": "Korpus 1"}, {"metric_value": "6.7", "corpus": "Korpus 1"}, {"metric_value": "6", "corpus": "Korpus 1"}, {
            "metric_value": "5.7",
            "corpus": "Korpus 1"
        }, {"metric_value": "5.5", "corpus": "Korpus 1"}, {"metric_value": "5.5", "corpus": "Korpus 1"}, {"metric_value": "5.8", "corpus": "Korpus 1"}, {
            "metric_value": "6",
            "corpus": "Korpus 1"
        }, {"metric_value": "5.4", "corpus": "Korpus 1"}, {"metric_value": "6", "corpus": "Korpus 1"}, {"metric_value": "6.7", "corpus": "Korpus 1"}, {
            "metric_value": "6.3",
            "corpus": "Korpus 1"
        }, {"metric_value": "5.6", "corpus": "Korpus 1"}, {"metric_value": "5.5", "corpus": "Korpus 1"}, {"metric_value": "5.5", "corpus": "Korpus 1"}, {
            "metric_value": "6.1",
            "corpus": "Korpus 1"
        }, {"metric_value": "5.8", "corpus": "Korpus 1"}, {"metric_value": "5", "corpus": "Korpus 1"}, {"metric_value": "5.6", "corpus": "Korpus 1"}, {
            "metric_value": "5.7",
            "corpus": "Korpus 1"
        }, {"metric_value": "5.7", "corpus": "Korpus 1"}, {"metric_value": "6.2", "corpus": "Korpus 1"}, {"metric_value": "5.1", "corpus": "Korpus 1"}, {"metric_value": "5.7", "corpus": "Korpus 1"}]
    }
        , {
            "section": "h2" , "rawData": [{"metric_value": "5.1", "corpus": "Korpus 1"}, {"metric_value": "4.9", "corpus": "Korpus 1"}, {"metric_value": "4.7", "corpus": "Korpus 1"}, {
                "metric_value": "4.6",
                "corpus": "Korpus 1"
            }, {"metric_value": "5", "corpus": "Korpus 1"}, {"metric_value": "5.4", "corpus": "Korpus 1"}, {"metric_value": "4.6", "corpus": "Korpus 1"}, {
                "metric_value": "5",
                "corpus": "Korpus 1"
            }, {"metric_value": "4.4", "corpus": "Korpus 1"}, {"metric_value": "4.9", "corpus": "Korpus 1"}, {"metric_value": "5.4", "corpus": "Korpus 1"}, {
                "metric_value": "4.8",
                "corpus": "Korpus 1"
            }, {"metric_value": "4.8", "corpus": "Korpus 1"}, {"metric_value": "4.3", "corpus": "Korpus 1"}, {"metric_value": "5.8", "corpus": "Korpus 1"}, {
                "metric_value": "5.7",
                "corpus": "Korpus 1"
            }, {"metric_value": "5.4", "corpus": "Korpus 1"}, {"metric_value": "5.1", "corpus": "Korpus 1"}, {"metric_value": "5.7", "corpus": "Korpus 1"}, {
                "metric_value": "5.1",
                "corpus": "Korpus 1"
            }, {"metric_value": "5.4", "corpus": "Korpus 1"}, {"metric_value": "5.1", "corpus": "Korpus 1"}, {"metric_value": "4.6", "corpus": "Korpus 1"}, {
                "metric_value": "5.1",
                "corpus": "Korpus 1"
            }, {"metric_value": "4.8", "corpus": "Korpus 1"}, {"metric_value": "5", "corpus": "Korpus 1"}, {"metric_value": "5", "corpus": "Korpus 1"}, {
                "metric_value": "5.2",
                "corpus": "Korpus 1"
            }, {"metric_value": "5.2", "corpus": "Korpus 1"}, {"metric_value": "4.7", "corpus": "Korpus 1"}, {"metric_value": "4.8", "corpus": "Korpus 1"}, {
                "metric_value": "5.4",
                "corpus": "Korpus 1"
            }, {"metric_value": "5.2", "corpus": "Korpus 1"}, {"metric_value": "5.5", "corpus": "Korpus 1"}, {"metric_value": "4.9", "corpus": "Korpus 1"}, {
                "metric_value": "5",
                "corpus": "Korpus 1"
            }, {"metric_value": "5.5", "corpus": "Korpus 1"}, {"metric_value": "4.9", "corpus": "Korpus 1"}, {"metric_value": "4.4", "corpus": "Korpus 1"}, {
                "metric_value": "5.1",
                "corpus": "Korpus 1"
            }, {"metric_value": "5", "corpus": "Korpus 1"}, {"metric_value": "4.5", "corpus": "Korpus 1"}, {"metric_value": "4.4", "corpus": "Korpus 1"}, {
                "metric_value": "5",
                "corpus": "Korpus 1"
            }, {"metric_value": "5.1", "corpus": "Korpus 1"}, {"metric_value": "4.8", "corpus": "Korpus 1"}, {"metric_value": "5.1", "corpus": "Korpus 1"}, {
                "metric_value": "4.6",
                "corpus": "Korpus 1"
            }, {"metric_value": "5.3", "corpus": "Korpus 1"}, {"metric_value": "5", "corpus": "Korpus 1"}, {"metric_value": "7", "corpus": "Korpus 2"}, {
                "metric_value": "6.4",
                "corpus": "Korpus 2"
            }, {"metric_value": "6.9", "corpus": "Korpus 2"}, {"metric_value": "5.5", "corpus": "Korpus 2"}, {"metric_value": "6.5", "corpus": "Korpus 2"}, {
                "metric_value": "5.7",
                "corpus": "Korpus 2"
            }, {"metric_value": "6.3", "corpus": "Korpus 2"}, {"metric_value": "4.9", "corpus": "Korpus 2"}, {"metric_value": "6.6", "corpus": "Korpus 2"}, {
                "metric_value": "5.2",
                "corpus": "Korpus 2"
            }, {"metric_value": "5", "corpus": "Korpus 2"}, {"metric_value": "5.9", "corpus": "Korpus 2"}, {"metric_value": "6", "corpus": "Korpus 2"}, {
                "metric_value": "6.1",
                "corpus": "Korpus 2"
            }, {"metric_value": "5.6", "corpus": "Korpus 2"}, {"metric_value": "6.7", "corpus": "Korpus 2"}, {"metric_value": "5.6", "corpus": "Korpus 2"}, {
                "metric_value": "5.8",
                "corpus": "Korpus 2"
            }, {"metric_value": "6.2", "corpus": "Korpus 2"}, {"metric_value": "5.6", "corpus": "Korpus 2"}, {"metric_value": "5.9", "corpus": "Korpus 2"}, {
                "metric_value": "6.1",
                "corpus": "Korpus 2"
            }, {"metric_value": "6.3", "corpus": "Korpus 2"}, {"metric_value": "6.1", "corpus": "Korpus 2"}, {"metric_value": "6.4", "corpus": "Korpus 2"}, {
                "metric_value": "6.6",
                "corpus": "Korpus 2"
            }, {"metric_value": "6.8", "corpus": "Korpus 2"}, {"metric_value": "6.7", "corpus": "Korpus 2"}, {"metric_value": "6", "corpus": "Korpus 2"}, {
                "metric_value": "5.7",
                "corpus": "Korpus 2"
            }, {"metric_value": "5.5", "corpus": "Korpus 2"}, {"metric_value": "5.5", "corpus": "Korpus 2"}, {"metric_value": "5.8", "corpus": "Korpus 2"}, {
                "metric_value": "6",
                "corpus": "Korpus 2"
            }, {"metric_value": "5.4", "corpus": "Korpus 2"}, {"metric_value": "6", "corpus": "Korpus 2"}, {"metric_value": "6.7", "corpus": "Korpus 2"}, {
                "metric_value": "6.3",
                "corpus": "Korpus 2"
            }, {"metric_value": "5.6", "corpus": "Korpus 2"}, {"metric_value": "5.5", "corpus": "Korpus 2"}, {"metric_value": "5.5", "corpus": "Korpus 2"}, {
                "metric_value": "6.1",
                "corpus": "Korpus 2"
            }, {"metric_value": "5.8", "corpus": "Korpus 2"}, {"metric_value": "5", "corpus": "Korpus 2"}, {"metric_value": "5.6", "corpus": "Korpus 2"}, {
                "metric_value": "5.7",
                "corpus": "Korpus 2"
            }, {"metric_value": "5.7", "corpus": "Korpus 2"}, {"metric_value": "6.2", "corpus": "Korpus 2"}, {"metric_value": "5.1", "corpus": "Korpus 2"}, {
                "metric_value": "5.7",
                "corpus": "Korpus 2"
            }]
        }]


    let statisticalData = sumstat;
    //TODO debug ^

    let metricSectionSelectorContainer = d3.select(htmlEl[0]).append("div").classed("metricSectionSelectorContainer", true);
    metricSectionSelectorContainer.append("p").text("Abschnitt:");
    let sectionSelector = metricSectionSelectorContainer.append("select").classed("metricSectionSelector", true);

        sectionSelector.selectAll("option").data(rawData).enter().append("option").attr("value", function(d) {return d.section}).text(function (d) {return d.section});
        sectionSelector.on("change", function () {console.log("datachangeld")});

    let metricContainer = d3.select(htmlEl[0]);

    let metricDescription = metricContainer.append("div").classed("metricDescription", true).classed("row", true);

    //Add a statistical overview for each corpus
    for (corpus of statisticalData) {
        console.log(corpus);

        let metricDescriptionCol = metricDescription.append("div").classed("col", true).attr("style", "display: inline-block;");
        metricDescriptionCol.append("div").classed("metricDescriptionColHeader", true).text(corpus.key);
        let metricDescriptionTags = metricDescriptionCol.append("div").classed("metricDescriptionColTags", true);

        //TODO keys abgleichen
        metricDescriptionTags.append("p").classed("metric-data modus-text", true).text(corpus.value.max.toFixed(2)).attr("data-before", "Modus: ");
        metricDescriptionTags.append("p").classed("metric-data median-text", true).text(corpus.value.median).attr("data-before", "Median: ");
        metricDescriptionTags.append("p").classed("metric-data average-text", true).text(corpus.value.q3).attr("data-before", "Durchschnitt: ");
        metricDescriptionTags.append("p").classed("metric-data variance-text", true).text(corpus.value.interQuantileRange.toFixed(2)).attr("data-before", "Varianz: ");
    };

    //drat the boxplot
    //drawBoxplot(metricContainer, statisticalData, rawData);

    //Create CSV file and download
    createCSVdownload(IDMetricEl, rawData);
};

function returnGraphTextSection(IDMetricEl, htmlEl, data2){
}

function returnGraphTextTotal(IDMetricEl, htmlEl, data2){
}


function drawBoxplot(container, statisticsData, dataPoints) {
    var margin = {top: 20, right: 40, bottom: 60, left: 120};

    let height = 200 - margin.bottom - margin.top;
    let width = 960 - margin.right - margin.left;

    let svg = container.append("div")
        .classed("graphContainer", true)
        .append("svg")
        .classed("svg-chart", true)
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 960 200")
        .append("g").attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


    //TODO domain dynamisch
    // Show the Y scale
    var y = d3.scaleBand()
        .range([height, 0])
        .domain(["Korpus 2", "Korpus 1"])
        .padding(.4);
    svg.append("g")
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain").remove()

    // Show the X scale
    var x = d3.scaleLinear()
        .domain([4, 8])
        .range([0, width])
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(5))
        .select(".domain").remove()

    // Color scale
    var myColor = d3.scaleSequential()
        .interpolator(d3.interpolateInferno)
        .domain([4, 8])

    // Show the main vertical line
    svg
        .selectAll("vertLines")
        .data(statisticsData)
        .enter()
        .append("line")
        .attr("x1", function (d) {
            return (x(d.value.min))
        })
        .attr("x2", function (d) {
            return (x(d.value.max))
        })
        .attr("y1", function (d) {
            return (y(d.key) + y.bandwidth() / 2)
        })
        .attr("y2", function (d) {
            return (y(d.key) + y.bandwidth() / 2)
        })
        .attr("stroke", "black")
        .style("width", 40)

    // rectangle for the main box
    svg
        .selectAll("boxes")
        .data(statisticsData)
        .enter()
        .append("rect")
        .attr("x", function (d) {
            return (x(d.value.q1))
        })
        .attr("width", function (d) {
            ;
            return (x(d.value.q3) - x(d.value.q1))
        })
        .attr("y", function (d) {
            return y(d.key);
        })
        .attr("height", y.bandwidth())
        .attr("stroke", "black")
        .style("fill", "#69b3a2")
        .style("opacity", 0.3)

    // Show the median
    svg
        .selectAll("medianLines")
        .data(statisticsData)
        .enter()
        .append("line")
        .attr("y1", function (d) {
            return (y(d.key) + y.bandwidth() / 2 + (height / 4))
        })
        .attr("y2", function (d) {
            return (y(d.key) + y.bandwidth() / 2 - (height / 4))
        })
        .attr("x1", function (d) {
            return (x(d.value.median))
        })
        .attr("x2", function (d) {
            return (x(d.value.median))
        })
        .attr("stroke", "black");


    // Add individual points with jitter
    var jitterWidth = 30;

    //TODO debug daten anpassen
    svg
        .selectAll("indPoints")
        .data(dataPoints)
        .enter()
        .append("circle")
        .attr("cx", function (d) {
            return (x(d.metric_value))
        })
        .attr("cy", function (d) {
            return (y(d.corpus) + (y.bandwidth() / 2) - jitterWidth / 2 + Math.random() * jitterWidth)
        })
        .attr("r", 4)
        .style("fill", function (d) {
            return (myColor(+d.metric_value))
        })
        .attr("stroke", "black")

}

function createCSVdownload(metricID, dataPoints) {

    let metric_name = metricID.split("_")[2]
    let downloadButton = d3.select("#download_" + metric_name);
    downloadButton.style("visibility", "visible");

    let csv_text = convertJSONtoCSV(dataPoints);

    //add CSV header
    csv_text = metric_name + "_values," + "corpus" + "\r\n" + csv_text;


    let csv_data = "data:text/plain;charset=utf-8," + encodeURIComponent(csv_text);
    downloadButton.attr("href", csv_data);
    downloadButton.attr("download", metric_name + "_csvdata");

    function convertJSONtoCSV(data) {

        let csv_text = "";

        for (let i = 0; i < data.length; i++) {
            let data_row = "";
            for (let col in data[i]) {
                if (data_row != "") {
                    data_row += ",";
                }
                data_row += data[i][col];
            }
            csv_text += data_row + "\r\n";
        }
        return csv_text;
    };
};


