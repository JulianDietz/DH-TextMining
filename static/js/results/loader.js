$(document).ready(function () {
    $(".toggle_button").click(function () {

        const textVariants = [{"key": "orig", "value": "Raw", "display": "Original"},
            {"key": "stpw", "value": "NltkStw", "display": "Stopwortgefiltert"},
            {"key": "stmd", "value": "NltkStem", "display": "Gestemmt"}];

        let $this = $(this);
        let collapseEl = $($this.attr("data-collapse"));

        let statisticDisplayType = $this.attr("data-statisticdisplaytype");

        if ($this.attr("data-ready") == "false") {
            $.ajax({
                url: calculateURL,
                type: 'GET',
                data: {fieldname: $this.attr("id").split('_')[2], Korpus1_variante: varianteKorpus1, Korpus2_variante: varianteKorpus2},
                beforeSend: function () {
                    $this.next().children(".indicator").attr("src", "/static/img/results/stopwatch.png");
                },
                success: function (response) {
                    onSuccess(JSON.parse(response));
                }
            });

            function onSuccess(data) {
                console.log(data);

                switch (statisticDisplayType) {
                    case "numeric-total":
                        returnGraphNumericTotal($this.attr("id"), collapseEl, data, textVariants);
                        break;
                    case "numeric-section":
                        returnGraphNumericSection($this.attr("id"), collapseEl, data, textVariants);
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
            }
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


function returnGraphNumericTotal(IDMetricEl, htmlEl, data, textVariants) {

    let metricName = IDMetricEl.split("_")[2];

    //HIER SIND ALLE INTERAKTIONEN
    //Section selector
    let metricSectionSelectorContainer = d3.select(htmlEl[0]).append("div").classed("metricSectionSelectorContainer", true).attr("id", "metricSectionSelectorContainer_" + IDMetricEl);
    metricSectionSelectorContainer.append("p").text("Diese Metrik bezieht sich auf das gesamte Dokument").style("display", "inline-block");

    //recalculate Metric
    recalcButton = metricSectionSelectorContainer.append("button").classed("btn-dh-white btn-rclc", true).text("Metrik neu berechnen")


    if (Object.keys(data[metricName]).length > 1) {
        //text Variante Korpus2
        let textVarSelect2 = metricSectionSelectorContainer
            .append("div")
            .classed("textVarSelectContainer", true)
            .text("Korpus 2:")
            .append("select")
            .classed("textVarSelect", true)
            .attr("id", "textVar_Korpus2_" + IDMetricEl);

        textVarSelect2
            .selectAll("option")
            .data(textVariants)
            .enter()
            .append("option")
            .attr("value", function (d) {
                return d.value;
            })
            .text(function (d) {
                return d.display;
            });

        //update selection for korpus2
        for (let i = 0; i < textVarSelect2.node().options.length; i++) {
            if (textVarSelect2.node().options[i].value === data[IDMetricEl.split("_")[2]].Corpus2.variant) {
                textVarSelect2.node().selectedIndex = i;
            }
            ;
        }
        ;
    }
    ;


    //Text Variante Korpus 1
    let textVarSelect1 = metricSectionSelectorContainer
        .append("div")
        .classed("textVarSelectContainer", true)
        .text("Korpus 1:")
        .append("select")
        .classed("textVarSelect", true)
        .attr("id", "textVar_Korpus1_" + IDMetricEl);

    textVarSelect1
        .selectAll("option")
        .data(textVariants)
        .enter()
        .append("option")
        .attr("value", function (d) {
            return d.value;
        })
        .text(function (d) {
            return d.display;
        });

    //update selection for korpus1
    for (let i = 0; i < textVarSelect1.node().options.length; i++) {
        if (textVarSelect1.node().options[i].value === data[metricName].Corpus1.variant) {
            textVarSelect1.node().selectedIndex = i;
        }
        ;
    }
    ;


    //recalculate function
    recalcButton.on("click", function () {
        selectedTextVar1 = d3.select("#textVar_Korpus1_" + IDMetricEl).node().options[d3.select("#textVar_Korpus1_" + IDMetricEl).node().selectedIndex].value;

        selectedTextVar2 = null;
        if ((Object.keys(data[metricName]).length > 1)) {
            selectedTextVar2 = d3.select("#textVar_Korpus2_" + IDMetricEl).node().options[d3.select("#textVar_Korpus2_" + IDMetricEl).node().selectedIndex].value;
        }
        recalculateMetric(IDMetricEl, selectedTextVar1, selectedTextVar2);
    });


    // HIER WERDEN DIE DATEN DER METRIK EINGEFÜLLT
    let metricContainer = d3.select(htmlEl[0]);

    let metricDescription = metricContainer.append("div").classed("metricDescription", true).classed("row", true).attr("id", "metricDescription_" + IDMetricEl);
    ;

    //Add a statistical overview for each corpus
    for (corpus in data[metricName]) {
        let metricDescriptionCol = metricDescription.append("div").classed("col", true).attr("style", "display: inline-block;");
        metricDescriptionCol.append("div").classed("metricDescriptionColHeader", true).text(corpus);
        let metricDescriptionTags = metricDescriptionCol.append("div").classed("metricDescriptionColTags", true);

        metricDescriptionTags.append("p").classed("metric-data modus-text", true).text(data[metricName][corpus].statisticalValues.mode.join(", ")).attr("data-before", "Modus: ");
        metricDescriptionTags.append("p").classed("metric-data median-text", true).text(data[metricName][corpus].statisticalValues.median.toFixed(2)).attr("data-before", "Median: ");
        metricDescriptionTags.append("p").classed("metric-data average-text", true).text(data[metricName][corpus].statisticalValues.average.toFixed(2)).attr("data-before", "Durchschnitt: ");
        metricDescriptionTags.append("p").classed("metric-data variance-text", true).text(data[metricName][corpus].statisticalValues.variance.toFixed(2)).attr("data-before", "Varianz: ");
    }
    ;

    let calcRawData = convertDataTotalNumericRawValues(data, metricName);
    let calcStatsticalData = convertDataTotalNumericStatistics(data, metricName);

    //drat the boxplot
    drawBoxplot(IDMetricEl, metricContainer, calcStatsticalData, calcRawData);

    //Create CSV file and download
    createCSVdownload(IDMetricEl, calcRawData);
};

function returnGraphNumericSection(IDMetricEl, htmlEl, data, textVariants) {
    //TODO debug v
    let sumstat = [
        {"key": "Korpus 1", "value": {"q1": 4.8, "median": 5, "q3": 5.2, "interQuantileRange": 0.40000000000000036, "min": 4.199999999999999, "max": 5.800000000000001}},
        {"key": "Korpus 2", "value": {"q1": 5.6, "median": 5.9, "q3": 6.3, "interQuantileRange": 0.7000000000000002, "min": 4.549999999999999, "max": 7.35}}]

    let rawData = [{
        "section": "h1", "rawData": [{"metric_value": "5.1", "corpus": "Korpus 2"}, {"metric_value": "4.9", "corpus": "Korpus 2"}, {"metric_value": "4.7", "corpus": "Korpus 2"}, {
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
            "section": "h2", "rawData": [{"metric_value": "5.1", "corpus": "Korpus 1"}, {"metric_value": "4.9", "corpus": "Korpus 1"}, {"metric_value": "4.7", "corpus": "Korpus 1"}, {
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

    let metricName = IDMetricEl.split("_")[2];

    //Section selector
    let metricSectionSelectorContainer = d3.select(htmlEl[0]).append("div").classed("metricSectionSelectorContainer", true);

    metricSectionSelectorContainer.append("p").text("Abschnitt:").style("display", "inline-block");
    let sectionSelector = metricSectionSelectorContainer.append("select").classed("paperAreaSelector", true);

    console.log(data);



        for (area in data[metricName].Corpus1.rawValues.sectioned) {
            for (section in data[metricName].Corpus1.rawValues.sectioned[area]) {
                console.log(section)
                sectionSelector.append("option").attr("value", area).text("Sektion: " + area + (parseInt(section)+1));
            }
        };
        ;
        for (area in data[metricName].Corpus1.rawValues.totals) {
            sectionSelector.append("option").attr("value", area).text("Gesamt: " + area);

        }
        ;



    /*.data(data).enter().append("option").attr("value", function (d) {
        console.log(d)
        return d.section
    }).text(function (d) {
        return d.section
    });*/


    sectionSelector.on("change", function () {
        console.log("Abschnitt changed");
    });

    //NEU
    //recalculate Metric
    recalcButton = metricSectionSelectorContainer.append("button").classed("btn-dh-white btn-rclc", true).text("Metrik neu berechnen")


    if (Object.keys(data[metricName]).length > 1) {
        //text Variante Korpus2
        let textVarSelect2 = metricSectionSelectorContainer
            .append("div")
            .classed("textVarSelectContainer", true)
            .text("Korpus 2:")
            .append("select")
            .classed("textVarSelect", true)
            .attr("id", "textVar_Korpus2_" + IDMetricEl);

        textVarSelect2
            .selectAll("option")
            .data(textVariants)
            .enter()
            .append("option")
            .attr("value", function (d) {
                return d.value;
            })
            .text(function (d) {
                return d.display;
            });

        //update selection for korpus2
        for (let i = 0; i < textVarSelect2.node().options.length; i++) {
            if (textVarSelect2.node().options[i].value === data[IDMetricEl.split("_")[2]].Corpus2.variant) {
                textVarSelect2.node().selectedIndex = i;
            }
            ;
        }
        ;
    }
    ;


    //Text Variante Korpus 1
    let textVarSelect1 = metricSectionSelectorContainer
        .append("div")
        .classed("textVarSelectContainer", true)
        .text("Korpus 1:")
        .append("select")
        .classed("textVarSelect", true)
        .attr("id", "textVar_Korpus1_" + IDMetricEl);

    textVarSelect1
        .selectAll("option")
        .data(textVariants)
        .enter()
        .append("option")
        .attr("value", function (d) {
            return d.value;
        })
        .text(function (d) {
            return d.display;
        });

    //update selection for korpus1
    for (let i = 0; i < textVarSelect1.node().options.length; i++) {
        if (textVarSelect1.node().options[i].value === data[metricName].Corpus1.variant) {
            textVarSelect1.node().selectedIndex = i;
        }
        ;
    }
    ;


    //recalculate function
    recalcButton.on("click", function () {
        selectedTextVar1 = d3.select("#textVar_Korpus1_" + IDMetricEl).node().options[d3.select("#textVar_Korpus1_" + IDMetricEl).node().selectedIndex].value;

        selectedTextVar2 = null;
        if ((Object.keys(data[metricName]).length > 1)) {
            selectedTextVar2 = d3.select("#textVar_Korpus2_" + IDMetricEl).node().options[d3.select("#textVar_Korpus2_" + IDMetricEl).node().selectedIndex].value;
        }
        recalculateMetric(IDMetricEl, selectedTextVar1, selectedTextVar2);
    });


    // HIER WERDEN DIE DATEN DER METRIK EINGEFÜLLT
    let metricContainer = d3.select(htmlEl[0]);

    let metricDescription = metricContainer.append("div").classed("metricDescription", true).classed("row", true).attr("id", "metricDescription_" + IDMetricEl);
    ;

    //Add a statistical overview for each corpus
    /*for (corpus in data[metricName]) {
        let metricDescriptionCol = metricDescription.append("div").classed("col", true).attr("style", "display: inline-block;");
        metricDescriptionCol.append("div").classed("metricDescriptionColHeader", true).text(corpus);
        let metricDescriptionTags = metricDescriptionCol.append("div").classed("metricDescriptionColTags", true);

        metricDescriptionTags.append("p").classed("metric-data modus-text", true).text(data[metricName][corpus].statisticalValues.mode.join(", ")).attr("data-before", "Modus: ");
        metricDescriptionTags.append("p").classed("metric-data median-text", true).text(data[metricName][corpus].statisticalValues.median.toFixed(2)).attr("data-before", "Median: ");
        metricDescriptionTags.append("p").classed("metric-data average-text", true).text(data[metricName][corpus].statisticalValues.average.toFixed(2)).attr("data-before", "Durchschnitt: ");
        metricDescriptionTags.append("p").classed("metric-data variance-text", true).text(data[metricName][corpus].statisticalValues.variance.toFixed(2)).attr("data-before", "Varianz: ");
    }
    ;*/

    //let calcRawData = convertDataTotalNumericRawValues(data, metricName);
    //let calcStatsticalData = convertDataTotalNumericStatistics(data, metricName);
    //NEU ENDE
    //drat the boxplot
    //drawBoxplot(metricContainer, calcStatisticalData, calcRawData);

    //Create CSV file and download
    //createCSVdownload(IDMetricEl, calcrawData);
};

function returnGraphTextSection(IDMetricEl, htmlEl, data2, textVariants) {
    console.log("test")
}

function returnGraphTextTotal(IDMetricEl, htmlEl, data2, textVariants) {
    console.log("test")
}


//General functions
function drawBoxplot(metricID, container, statisticsData, dataPoints) {
    var margin = {top: 20, right: 40, bottom: 60, left: 120};

    let height = 200 - margin.bottom - margin.top;
    let width = 960 - margin.right - margin.left;

    let svg = container.append("div")
        .classed("graphContainer", true)
        .attr("id", "graphContainer_" + metricID)
        .append("svg")
        .classed("svg-chart", true)
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 960 200")
        .append("g").attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    //Create domain
    let domainY = [];
    let domainX = [[], []];
    for (corpus of statisticsData) {
        domainY.unshift(corpus.corpus);
        domainX[0].push([corpus.value.minimum]);
        domainX[1].push([corpus.value.maximum]);
    }
    ;

    let min = d3.max([0, parseInt(d3.min(domainX[0])) - 1]);
    let max = parseInt(d3.max(domainX[1])) + 1;

    // Show the Y scale
    var y = d3.scaleBand()
        .range([height, 0])
        .domain(domainY)
        .padding(.4);
    svg.append("g")
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain").remove()


    // Show the X scale
    var x = d3.scaleLinear()
        .domain([min, max])
        .range([0, width])
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(5))
        .select(".domain").remove()

    // Color scale
    var myColor = d3.scaleSequential()
        .interpolator(d3.interpolateInferno)
        .domain([min, max])

    // Show the main vertical line
    svg
        .selectAll("vertLines")
        .data(statisticsData)
        .enter()
        .append("line")
        .attr("x1", function (d) {
            return (x(d.value.minimum))
        })
        .attr("x2", function (d) {
            return (x(d.value.maximum))
        })
        .attr("y1", function (d) {
            return (y(d.corpus) + y.bandwidth() / 2)
        })
        .attr("y2", function (d) {
            return (y(d.corpus) + y.bandwidth() / 2)
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
            return (x(d.value.lowerQuartile))
        })
        .attr("width", function (d) {
            ;
            return (x(d.value.upperQuartile) - x(d.value.lowerQuartile))
        })
        .attr("y", function (d) {
            return y(d.corpus);
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
            return (y(d.corpus) + y.bandwidth() / 2 + (height / 4))
        })
        .attr("y2", function (d) {
            return (y(d.corpus) + y.bandwidth() / 2 - (height / 4))
        })
        .attr("x1", function (d) {
            return (x(d.value.median))
        })
        .attr("x2", function (d) {
            return (x(d.value.median))
        })
        .attr("stroke", "black");

    //tooltip
    let tooltip = container
        .append("div")
        .style("opacity", 0)
        .classed("tooltip-cust", true)
        .attr("id", metricID + "_tooltip");

    let mouseover = function (d) {

        tooltip
            .transition()
            .duration(200)
            .style("opacity", 1);
        tooltip
            .html("<span style='color:grey'>Titel: </span>" + d.values.paperTitle + " (" + d.values.year + ") " + d.values.authors[0]);
    };
    let mouseleave = function (d) {
        tooltip
            .transition()
            .duration(200)
            .style("opacity", 0)
    };


    // Add individual points with jitter
    let jitterWidth = 30;
    svg
        .selectAll("indPoints")
        .data(dataPoints)
        .enter()
        .append("circle")
        .attr("cx", function (d) {
            return (x(d.values.value))
        })
        .attr("cy", function (d) {
            return (y(d.corpus) + (y.bandwidth() / 2) - jitterWidth / 2 + Math.random() * jitterWidth)
        })
        .attr("r", 4)
        .style("fill", function (d) {
            return (myColor(+d.values.value))
        })
        .attr("stroke", "black")
        .on("mouseover", mouseover)
        .on("mouseleave", mouseleave)

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

function recalculateMetric(metricID, textVariantKorpus1, textVarianteKorpus2) {
    console.log(metricID);
    $.ajax({
        url: calculateURL,
        type: 'GET',
        data: {fieldname: metricID.split('_')[2], Korpus1_variante: textVariantKorpus1, Korpus2_variante: textVarianteKorpus2},
        beforeSend: function () {
            console.log("beforeSend");
            $("#collapse_button_" + metricID).next().children(".indicator").attr("src", "/static/img/results/stopwatch.png");
        },
        success: function (response) {
            console.log(response);
            onSuccess(JSON.parse(response));
        }
    });

    function onSuccess(data) {

        d3.select("#metricDescription_" + metricID).remove();
        d3.select("#metricSectionSelectorContainer_" + metricID).remove();
        d3.select("#graphContainer_" + metricID).remove();
        d3.select("#" + metricID + "_tooltip").remove();

        const textVariants = [{"key": "orig", "value": "Raw", "display": "Original"},
            {"key": "stpw", "value": "NltkStw", "display": "Stopwortgefiltert"},
            {"key": "stmd", "value": "NltkStem", "display": "Gestemmt"}];

        let collapseEl = $($('#' + metricID).attr("data-collapse"));
        let statisticDisplayType = $('#' + metricID).attr("data-statisticdisplaytype");


        switch (statisticDisplayType) {
            case "numeric-total":
                returnGraphNumericTotal(metricID, collapseEl, data, textVariants);
                break;
            case "numeric-section":
                returnGraphNumericSection(metricID, collapseEl, data, textVariants);
                break;
            case "text-total":

                break;
            case "text-section":
                break;
        }

        //d3.select('#' + metricID).attr("data-ready", "true");
        $("#collapse_button_" + metricID).next().children(".indicator").attr("src", "/static/img/results/verified.png")
    }
}


//Converters
function convertDataTotalNumericStatistics(data, metricName) {
    statisticsArr = []
    for (corpus in data[metricName]) {
        statisticsArr.push({"corpus": corpus, "value": data[metricName][corpus].statisticalValues});
    }
    ;
    return statisticsArr;
};

function convertDataTotalNumericRawValues(data, metricName) {
    let rawValuesArr = [];

    for (corpus in data[metricName]) {
        for (entry of data[metricName][corpus].rawValues) {
            rawValuesArr.push({"corpus": corpus, "values": entry});
        }
        ;
    }
    ;

    return rawValuesArr;
}


