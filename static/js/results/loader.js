$(document).ready(function () {
    $(".toggle_button").click(function () {

        const textVariants = [{"key": "orig", "value": "Raw", "display": "Original"},
            {"key": "stpw", "value": "NltkStw", "display": "Stopwortgefiltert"},
            {"key": "stmd", "value": "NltkStem", "display": "Gestemmt"}];

        let $this = $(this);

        let collapseEl = $($this.attr("data-collapse"));

        let statisticDisplayType = $this.attr("data-statisticdisplaytype");
        let graphType = $this.attr("data-graphtype");
        let allowTextVariants = ($this.attr("data-allowTextVariants").toString().trim() === "true");
        let foundation = $this.attr("data-foundation");

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
                addDownload(data, ($this.attr("id")));
                switch (statisticDisplayType) {
                    case "numeric-total":
                        returnGraphNumericTotal($this.attr("id"), collapseEl, data, textVariants, graphType, allowTextVariants, foundation);
                        break;
                    case "numeric-section":
                        returnGraphNumericSection($this.attr("id"), collapseEl, data, textVariants, graphType, allowTextVariants);
                        break;
                    case "text-total":
                        returnGraphTextTotal($this.attr("id"), collapseEl, data, textVariants, graphType, allowTextVariants, foundation)
                        break;
                    case "text-section":
                        break;
                }
                $this.toggleClass("toggle_button_closed").toggleClass("toggle_button_open");
                collapseEl.collapse('toggle');
                $this.attr("data-ready", "true");
                $this.next().children(".indicator").attr("src", "/static/img/results/verified.png");

                function addDownload(data, metricID) {
                    for (key of Object.keys(data[metricID.split("_")[2]])) {
                        let corpusNum = key.substring(6, 7);
                        d3.select("#download_section").append("a").classed("btn-dh-white", true).attr("href", "/textMining/downloadCorpus/Korpus" + corpusNum).text("Korpus " + corpusNum + " herunterladen");

                        //<a class="btn-dh-white" href="{% url 'downloadKorpus' "Korpus1" %}">Download Korpus1</a>
                    }
                }
            }
        }
        else
            {
                $(collapseEl).collapse('toggle');
                $this.toggleClass("toggle_button_closed").toggleClass("toggle_button_open");
            }
        }
    );

    $(".collapse").on('show.bs.collapse', function () {
    });

    $(".collapse").on('hide.bs.collapse', function () {
    });
});


function returnGraphNumericTotal(IDMetricEl, htmlEl, data, textVariants, graphType, allowTextVariants, foundation) {

    let metricName = IDMetricEl.split("_")[2];

    //HIER SIND ALLE INTERAKTIONEN
    //Section selector
    let metricSectionSelectorContainer = d3.select(htmlEl[0]).append("div").classed("metricSectionSelectorContainer", true).attr("id", "metricSectionSelectorContainer_" + IDMetricEl);

    let info = "";
    if (foundation === "document") {
        info = "Diese Metrik bezieht sich auf das gesamte Dokument";
    } else if (foundation === "corpus") {
        info = "Diese Metrik bezieht sich auf den gesamten Corpus";
    }

    metricSectionSelectorContainer.append("p").text(info).style("display", "inline-block");

    if (allowTextVariants) {
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
                .attr("id", "textVar_Corpus2_" + IDMetricEl)
                .on("change", function () {
                    $("#" + IDMetricEl).next().children(".indicator").attr("src", "/static/img/results/not-available.png");
                });

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
                })
                .on("change", function () {
                    $("#" + IDMetricEl).next().children(".indicator").attr("src", "/static/img/results/not-available.png");
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
            .attr("id", "textVar_Corpus1_" + IDMetricEl);

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
            selectedTextVar1 = d3.select("#textVar_Corpus1_" + IDMetricEl).node().options[d3.select("#textVar_Corpus1_" + IDMetricEl).node().selectedIndex].value;

            selectedTextVar2 = null;
            if ((Object.keys(data[metricName]).length > 1)) {
                selectedTextVar2 = d3.select("#textVar_Corpus2_" + IDMetricEl).node().options[d3.select("#textVar_Corpus2_" + IDMetricEl).node().selectedIndex].value;
            }
            recalculateMetric(IDMetricEl, selectedTextVar1, selectedTextVar2);
        });
    }
    ;


    // HIER WERDEN DIE DATEN DER METRIK EINGEFÜLLT
    let metricContainer = d3.select(htmlEl[0]);

    let metricDescription = metricContainer.append("div").classed("metricDescription", true).classed("row", true).attr("id", "metricDescription_" + IDMetricEl);

    //Add a statistical overview for each corpus

    for (corpus in data[metricName]) {

        let metricDescriptionCol = metricDescription.append("div").classed("col", true).attr("style", "display: inline-block;");
        metricDescriptionCol.append("div").classed("metricDescriptionColHeader", true).text(corpus);
        let metricDescriptionTags = metricDescriptionCol.append("div").classed("metricDescriptionColTags", true);

        let mod = data[metricName][corpus].statisticalValues.mode.join(", ")
        let med = data[metricName][corpus].statisticalValues.median.toFixed(2)
        let avg = data[metricName][corpus].statisticalValues.average.toFixed(2)
        let std = data[metricName][corpus].statisticalValues.std.toFixed(2)
        let cnt = data[metricName][corpus].statisticalValues.count.toFixed(0)

        createStatElement(metricDescriptionTags, mod, med, avg, std, cnt);
    }
    ;

    let calcRawData = convertDataTotalNumericRawValues(data, metricName);
    let calcStatsticalData = convertDataTotalNumericStatistics(data, metricName);

    //drat the boxplot
    drawGraph(IDMetricEl, metricContainer, calcStatsticalData, calcRawData, graphType);

    //Create CSV file and download
    createCSVdownload(IDMetricEl, calcRawData);
};

function returnGraphNumericSection(IDMetricEl, htmlEl, data, textVariants, graphType, allowTextVariants) {
    let metricName = IDMetricEl.split("_")[2];

    //Section selector
    let metricSectionSelectorContainer = d3.select(htmlEl[0]).append("div").classed("metricSectionSelectorContainer", true).attr("id", "metricSectionSelectorContainer_" + IDMetricEl);

    metricSectionSelectorContainer.append("p").text("Abschnitt:").style("display", "inline-block");
    let sectionSelector = metricSectionSelectorContainer.append("select").classed("paperAreaSelector", true);

    for (area in data[metricName].Corpus1.rawValues.totals) {
        sectionSelector.append("option").attr("value", area).text(area);
    }
    ;

    sectionSelector.on("change", function () {
        d3.select("#metricDescription_" + IDMetricEl).remove();
        d3.select("#graphContainer_" + IDMetricEl).remove();
        d3.select("#" + IDMetricEl + "_tooltip").remove();
        drawInfo();
    });

    if (allowTextVariants) {
        //NEU
        //recalculate Metric
        recalcButton = metricSectionSelectorContainer.append("button").classed("btn-dh-white btn-rclc", true).text("Metrik neu berechnen")

        //text Variant selector
        if (Object.keys(data[metricName]).length > 1) {
            //text Variante Korpus2
            let textVarSelect2 = metricSectionSelectorContainer
                .append("div")
                .classed("textVarSelectContainer", true)
                .text("Korpus 2:")
                .append("select")
                .classed("textVarSelect", true)
                .attr("id", "textVar_Corpus2_" + IDMetricEl)
                .on("change", function () {
                    $("#" + IDMetricEl).next().children(".indicator").attr("src", "/static/img/results/not-available.png");
                });

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
                })
            ;

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
            .attr("id", "textVar_Corpus1_" + IDMetricEl)
            .on("change", function () {
                $("#" + IDMetricEl).next().children(".indicator").attr("src", "/static/img/results/not-available.png");
            });
        ;

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
            })

        ;

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
            selectedTextVar1 = d3.select("#textVar_Corpus1_" + IDMetricEl).node().options[d3.select("#textVar_Corpus1_" + IDMetricEl).node().selectedIndex].value;

            selectedTextVar2 = null;
            if ((Object.keys(data[metricName]).length > 1)) {
                selectedTextVar2 = d3.select("#textVar_Corpus2_" + IDMetricEl).node().options[d3.select("#textVar_Corpus2_" + IDMetricEl).node().selectedIndex].value;
            }
            recalculateMetric(IDMetricEl, selectedTextVar1, selectedTextVar2);
        });
    }
    ;

    let createCSVdownloadfromArrayF = createCSVdownloadfromArray;
    //draw the table for the first time
    drawInfo();


    // HIER WERDEN DIE DATEN DER METRIK EINGEFÜLLT
    function drawInfo() {
        let metricContainer = d3.select(htmlEl[0]);

        let metricDescription = metricContainer.append("div").classed("metricDescription", true).classed("row", true).attr("id", "metricDescription_" + IDMetricEl);
        ;

        let tableEl = metricDescription.append("table").classed("table", true);
        let tableHeader = tableEl.append("thead").append("tr");
        let areaSelected = sectionSelector.node().options[sectionSelector.node().selectedIndex].value;


        //data table
        tableEl = tableEl.append("tbody");
        let tableTotalRow = tableEl.append("tr");
        tableTotalRow.append("th").text("Gesamt");
        tableTotalRow.append("th").append("i").classed("fas fa-chart-bar graph-icon_" + metricName, true).style("color", "lightgrey").style("cursor", "pointer").on("click", function () {
            let all = d3.selectAll(".graph-icon_" + metricName).style("color", "lightgrey");
            d3.select(this).style("color", "black");
            updateGraph(areaSelected, "totals");
        });

        tableHeader.append("th").text("Bereich");
        tableHeader.append("th").text("Graph");

        let csvBaseDataRawValues = [];

        //header and Total
        for (corpus in data[metricName]) {
            tableHeader.append("th").text(corpus);

            let cell = tableTotalRow.append("td")
            let mod = data[metricName][corpus].statisticalValues.totals[areaSelected].mode != undefined ? data[metricName][corpus].statisticalValues.totals[areaSelected].mode[0].toFixed(2) : "-";
            let med = data[metricName][corpus].statisticalValues.totals[areaSelected].median != undefined ? data[metricName][corpus].statisticalValues.totals[areaSelected].median.toFixed(2) : "-";
            let avg = data[metricName][corpus].statisticalValues.totals[areaSelected].average != undefined ? data[metricName][corpus].statisticalValues.totals[areaSelected].average.toFixed(2) : "-";
            let std = data[metricName][corpus].statisticalValues.totals[areaSelected].std != undefined ? data[metricName][corpus].statisticalValues.totals[areaSelected].std.toFixed(2) : "-";
            let cnt = data[metricName][corpus].statisticalValues.totals[areaSelected].count != undefined ? data[metricName][corpus].statisticalValues.totals[areaSelected].count.toFixed(0) : "-";

            createStatElement(cell, mod, med, avg, std, cnt);

            csvBaseDataRawValues.push({"corpus": corpus, "values": data[metricName][corpus].rawValues.totals[areaSelected], "section": areaSelected, "sectionNum": "totals"});
        }

        //Add a statistical overview for each corpus
        for (area in data[metricName].Corpus1.statisticalValues.sectioned[areaSelected]) {

            let row = tableEl.append("tr")
            row.append("th").attr("scope", "row").text(areaSelected + " " + (parseInt(area) + 1));
            row.append("th").append("i").classed("fas fa-chart-bar graph-icon_" + metricName, true).style("color", "lightgrey").style("cursor", "pointer").attr("data-sectionNum", area).on("click", function () {
                d3.selectAll(".graph-icon_" + metricName).style("color", "lightgrey");
                d3.select(this).style("color", "black");
                updateGraph(areaSelected, d3.select(this).attr("data-sectionNum"))
            });
            ;
            for (corpus in data[metricName]) {

                let cell = row.append("td")
                let mod = data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].mode != undefined ? data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].mode[0].toFixed(2) : "-";
                let med = data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].median != undefined ? data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].median.toFixed(2) : "-";
                let avg = data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].average != undefined ? data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].average.toFixed(2) : "-";
                let std = data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].std != undefined ? data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].std.toFixed(2) : "-";
                let cnt = data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].count != undefined ? data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].count.toFixed(0) : "-";

                createStatElement(cell, mod, med, avg, std, cnt);

                csvBaseDataRawValues.push({"corpus": corpus, "values": data[metricName][corpus].rawValues.sectioned[areaSelected][area], "section": areaSelected, "sectionNum": area});
            }
            ;
        }
        ;

        //Create CSV file and download
        createCSVdownloadfromArrayF(IDMetricEl, csvBaseDataRawValues);

        function updateGraph(section, sectionNum) {

            d3.select("#graphContainer_" + IDMetricEl).remove();
            d3.select("#" + IDMetricEl + "_tooltip").remove();

            let calcRawData = convertDataSectionNumericRawValues(data, metricName, section, sectionNum);
            let calcStatisticalData = convertDataSectionNumericStatistics(data, metricName, section, sectionNum);

            //NEU ENDE
            //draw the boxplot
            drawGraph(IDMetricEl, metricContainer, calcStatisticalData, calcRawData, graphType);
        }
    };
};

function returnGraphTextTotal(IDMetricEl, htmlEl, data, textVariants, graphType, allowTextVariants, foundation) {
    let metricName = IDMetricEl.split("_")[2];

    //HIER SIND ALLE INTERAKTIONEN
    //Section selector
    let metricSectionSelectorContainer = d3.select(htmlEl[0]).append("div").classed("metricSectionSelectorContainer", true).attr("id", "metricSectionSelectorContainer_" + IDMetricEl);

    let info = "";
    if (foundation === "document") {
        info = "Diese Metrik bezieht sich auf das gesamte Dokument";
    } else if (foundation === "corpus") {
        info = "Diese Metrik bezieht sich auf den gesamten Corpus";
    }

    metricSectionSelectorContainer.append("p").text(info).style("display", "inline-block");


    if (allowTextVariants) {
        //recalculate Metric
        recalcButton = metricSectionSelectorContainer.append("button").classed("btn-dh-white btn-rclc", true).text("Metrik neu berechnen");

        if (Object.keys(data[metricName]).length > 1) {
            //text Variante Korpus2
            let textVarSelect2 = metricSectionSelectorContainer
                .append("div")
                .classed("textVarSelectContainer", true)
                .text("Korpus 2:")
                .append("select")
                .classed("textVarSelect", true)
                .attr("id", "textVar_Corpus2_" + IDMetricEl)
                .on("change", function () {
                    $("#" + IDMetricEl).next().children(".indicator").attr("src", "/static/img/results/not-available.png");
                });

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
                })
                .on("change", function () {
                    $("#" + IDMetricEl).next().children(".indicator").attr("src", "/static/img/results/not-available.png");
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
            .attr("id", "textVar_Corpus1_" + IDMetricEl);

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
            selectedTextVar1 = d3.select("#textVar_Corpus1_" + IDMetricEl).node().options[d3.select("#textVar_Corpus1_" + IDMetricEl).node().selectedIndex].value;

            selectedTextVar2 = null;
            if ((Object.keys(data[metricName]).length > 1)) {
                selectedTextVar2 = d3.select("#textVar_Corpus2_" + IDMetricEl).node().options[d3.select("#textVar_Corpus2_" + IDMetricEl).node().selectedIndex].value;
            }
            recalculateMetric(IDMetricEl, selectedTextVar1, selectedTextVar2);
        });
    }
    ;

    // HIER WERDEN DIE DATEN DER METRIK EINGEFÜLLT
    let metricContainer = d3.select(htmlEl[0]);

    /*let metricDescription = metricContainer.append("div").classed("metricDescription", true).classed("row", true).attr("id", "metricDescription_" + IDMetricEl);
    ;

    //Add a statistical overview for each corpus
    for (corpus in data[metricName]) {
        let metricDescriptionCol = metricDescription.append("div").classed("col", true).attr("style", "display: inline-block;");
        metricDescriptionCol.append("div").classed("metricDescriptionColHeader", true).text(corpus);
        let metricDescriptionTags = metricDescriptionCol.append("div").classed("metricDescriptionColTags", true);

        metricDescriptionTags.append("p").classed("metric-data modus-text", true).text(data[metricName][corpus].statisticalValues.mode.join(", ")).attr("data-before", "Mod: ");
        metricDescriptionTags.append("p").classed("metric-data median-text", true).text(data[metricName][corpus].statisticalValues.median.toFixed(2)).attr("data-before", "Med: ");
        metricDescriptionTags.append("p").classed("metric-data average-text", true).text(data[metricName][corpus].statisticalValues.average.toFixed(2)).attr("data-before", "Avg: ");
        metricDescriptionTags.append("p").classed("metric-data variance-text", true).text(data[metricName][corpus].statisticalValues.variance.toFixed(2)).attr("data-before", "Var: ");
    }
    ;*/

    let calcRawData = convertDataTotalNumericRawValues(data, metricName);
    let calcStatisticalData = convertDataTotalNumericStatistics(data, metricName);

    //drat the boxplot
    drawGraph(IDMetricEl, metricContainer, calcStatisticalData, calcRawData, graphType);

    //Create CSV file and download
    createCSVdownload(IDMetricEl, calcRawData);
}


//General functions
function drawBoxplotGraph(metricID, container, statisticsData, dataPoints) {
    var margin = {top: 20, right: 60, bottom: 60, left: 60};

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
        domainX[0].push(corpus.value.minimum);
        domainX[1].push(corpus.value.maximum);
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
            return (x(d3.max([min, d.value.lowerQuartile - 1.5 * (d.value.upperQuartile - d.value.lowerQuartile)])));
        })
        .attr("x2", function (d) {
            return (x(d3.min([max, d.value.upperQuartile + 1.5 * (d.value.upperQuartile - d.value.lowerQuartile)])));
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
        d3.select(this).style("stroke-width", "2px");

        tooltip
            .transition()
            .duration(200)
            .style("opacity", 1);
        tooltip
            .html("<span style='color:grey'>Wert: </span>" + d.values.value + "<span style='color:grey'> Titel: </span>" + d.values.name + " (" + d.values.year + ") " + d.values.authors[0]);
    };

    let mouseleave = function (d) {
        tooltip
            .transition()
            .duration(200)
            .style("opacity", 0)

        d3.select(this).style("stroke-width", "1px");
    };

    //Brush
    svg.call(d3.brush()
        .extent([[0, 0], [width, height]])
        .on("start brush", displaySelection))


    function displaySelection() {
        extent = d3.event.selection;
        jitter.classed("jitter-selected_" + metricID, function (d) {
            return isBrushed(extent, (x(d.values.value)), (y(d.corpus) + (y.bandwidth() / 2) - jitterWidth / 2 + Math.random() * jitterWidth))
        });

        tooltip.html("<span style='color:grey'>Markiert: </span>" + d3.selectAll(".jitter-selected_" + metricID).size()).style("opacity", 1);

        function isBrushed(brush_coords, cx, cy) {

            let x0 = brush_coords[0][0],
                x1 = brush_coords[1][0],
                y0 = brush_coords[0][1],
                y1 = brush_coords[1][1];
            return x0 <= cx && cx <= x1 && y0 <= cy && cy <= y1;

        }
    }


    // Add individual points with jitter
    let jitterWidth = 30;
    let jitter = svg
        .selectAll("circle")
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
        .on("mousedown", function (d) {
            let e = brush.extent(),
                m = d3.mouse(svg.node()),
                p = [x.invert(m[0]), y.invert(m[1])];

            if (brush.empty() ||
                (e[0][0] > d[0] || d[0] > e[1][0]
                    || e[0][1] > d[1] || d[1] > e[1][1])
            ) {
                brush.extent([p, p]);
            } else {
                d3.select(this).classed('extent', true);
            }

        });

}

function drawLollipopGraph(metricID, container, statisticsData, dataPoints) {
    let margin = {top: 20, right: 60, bottom: 60, left: 60};

    let height = 300 - margin.bottom - margin.top;
    let width = 960 - margin.right - margin.left

    let svg = container.append("div")
        .classed("graphContainer", true)
        .attr("id", "graphContainer_" + metricID)
        .append("svg")
        .classed("svg-chart", true)
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 960 300")
        .append("g").attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    //Sort points by Data
    dataPoints.sort(function (a, b) {
        return a.values.value - b.values.value;
    });

    dataPoints = dataPoints.slice(dataPoints.length < 22 ? 0 : dataPoints.length - 21, dataPoints.length - 1);

    //Create domain
    let domainY = dataPoints.map(function (d) {
        return d.values.name
    });
    let domainX = [0, dataPoints[dataPoints.length - 1].values.value];

    // Show the Y scale
    let y = d3.scaleBand()
        .range([height, 0])
        .domain(domainY)
        .padding(.4);
    svg.append("g")
        .call(d3.axisLeft(y));


    // Show the X scale
    let x = d3.scaleLinear()
        .domain(domainX)
        .range([0, width])
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));


    // Color scale
    let myColor = d3.scaleSequential()
        .interpolator(d3.interpolateCool)
        .domain([height, 0]);

    //Create the lines
    svg.selectAll("lolli-lines")
        .data(dataPoints)
        .enter()
        .append("line")
        .attr("x1", function (d) {
            return x(d.values.value)
        })
        .attr("x2", x(0))
        .attr("y1", function (d) {
            return y(d.values.name)
        })
        .attr("y2", function (d) {
            return y(d.values.name)
        })
        .attr("stroke", "#d1d1d1");

    //tooltip
    let tooltip = container
        .append("div")
        .style("opacity", 0)
        .classed("tooltip-cust", true)
        .attr("id", metricID + "_tooltip");

    let mouseover = function (d) {
        d3.select(this).style("stroke-width", "2px");

        tooltip
            .transition()
            .duration(200)
            .style("opacity", 1);
        tooltip
            .html("<span style='color:grey'>Wert: </span>" + d.values.value + "<span style='color:grey'>Wort: </span>" + d.values.name);
    };

    let mouseleave = function (d) {
        tooltip
            .transition()
            .duration(200)
            .style("opacity", 0)

        d3.select(this).style("stroke-width", "1px");
    };

    svg.selectAll("lolli-circles")
        .data(dataPoints)
        .enter()
        .append("circle")
        .attr("cx", function (d) {
            return x(d.values.value);
        })
        .attr("cy", function (d) {
            return y(d.values.name);
        })
        .attr("r", "7")
        .style("fill", function (d) {
            return myColor(y(d.values.name))
        })
        .attr("stroke", "black")
        .on("mouseover", mouseover)
        .on("mouseleave", mouseleave)


}

function drawDoubleLollipopGraph(metricID, container, statisticsData, dataPoints) {
    let margin = {top: 20, right: 60, bottom: 60, left: 60};

    let height = 300 - margin.bottom - margin.top;
    let width = ((960 - margin.right - margin.left) / 2) - 20

    let svg = container.append("div")
        .classed("graphContainer", true)
        .attr("id", "graphContainer_" + metricID);

    let svgLeft = svg.append("svg")
        .style("width", "50%")
        //.classed("svg-chart", true)
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 480 300")
        .append("g").attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


    let svgRight = svg.append("svg")
    //.classed("svg-chart", true)
        .style("width", "50%")
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 480 300")
        .append("g").attr("transform",
            "translate(" + 20 + "," + margin.top + ")");


    //Sort points by Data
    dataPoints.sort(function (a, b) {
        return a.values.value - b.values.value;
    });

    //Create domain X
    let domainXRight = [dataPoints[dataPoints.length - 1].values.value, 0];

    let domainXLeft = [0, dataPoints[dataPoints.length - 1].values.value];


    let dataCorpusLeft = dataPoints.filter(el => el.corpus == "Corpus1");
    let dataCorpusRight = dataPoints.filter(el => el.corpus == "Corpus2");

    dataCorpusLeft = dataCorpusLeft.slice(dataCorpusLeft.length < 22 ? 0 : dataCorpusLeft.length - 21, dataCorpusLeft.length - 1);
    dataCorpusRight = dataCorpusRight.slice(dataCorpusRight.length < 22 ? 0 : dataCorpusRight.length - 21, dataCorpusRight.length - 1);


    //Create domain Y now with filter
    let domainYRight = dataCorpusRight.map(function (d) {
        return d.values.name;
    });

    let domainYLeft = dataCorpusLeft.map(function (d) {
        return d.values.name;
    });


    //RIGHT SIDE
    // Show the Y scale
    let yRight = d3.scaleBand()
        .range([height, 0])
        .domain(domainYRight)
        .padding(.6);
    svgRight.append("g")
        .attr("transform", "translate(" + width + "," + 0 + ")")
        .call(d3.axisRight(yRight));

    // Show the X scale
    let xRight = d3.scaleLinear()
        .domain(domainXRight)
        .range([0, width])
    svgRight.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xRight));

    //LEFT SIDE
    // Show the Y scale
    let yLeft = d3.scaleBand()
        .range([height, 0])
        .domain(domainYLeft)
        .padding(.6);
    svgLeft.append("g")
        .call(d3.axisLeft(yLeft));

    // Show the X scale
    let xLeft = d3.scaleLinear()
        .domain(domainXLeft)
        .range([0, width])
    svgLeft.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xLeft));


    // Color scale
    let myColor = d3.scaleSequential()
        .interpolator(d3.interpolateCool)
        .domain(domainXLeft);

    //tooltip
    let tooltip = container
        .append("div")
        .style("opacity", 0)
        .classed("tooltip-cust", true)
        .attr("id", metricID + "_tooltip");


    addData(svgLeft, xLeft, yLeft, dataCorpusLeft, tooltip);
    addData(svgRight, xRight, yRight, dataCorpusRight, tooltip);


    function addData(svgEl, x, y, dataPointsFil, tooltip) {
        //Create the lines
        svgEl.selectAll("lolli-lines")
            .data(dataPointsFil)
            .enter()
            .append("line")
            .attr("x1", function (d) {
                return x(d.values.value)
            })
            .attr("x2", x(0))
            .attr("y1", function (d) {
                return y(d.values.name)
            })
            .attr("y2", function (d) {
                return y(d.values.name)
            })
            .attr("stroke", "#d1d1d1");

        let mouseover = function (d) {
            d3.select(this).style("stroke-width", "2px");

            tooltip
                .transition()
                .duration(200)
                .style("opacity", 1);
            tooltip
                .html("<span style='color:grey'>Wert: </span>" + d.values.value + "<span style='color:grey'> Wort: </span>" + d.values.name + "<span style='color:grey'> Korpus: </span>" + d.corpus);
        };

        let mouseleave = function (d) {
            tooltip
                .transition()
                .duration(200)
                .style("opacity", 0)

            d3.select(this).style("stroke-width", "1px");
        };

        //Create the top
        svgEl.selectAll("lolli-circles")
            .data(dataPointsFil)
            .enter()
            .append("circle")
            .attr("cx", function (d) {
                return x(d.values.value);
            })
            .attr("cy", function (d) {
                return y(d.values.name);
            })
            .attr("r", "7")
            .style("fill", function (d) {
                return myColor(d.values.value);
            })
            .attr("stroke", "black")
            .on("mouseover", mouseover)
            .on("mouseleave", mouseleave)
    };

}

function drawWordCloudGraph(metricID, container, statisticsData, dataPoints) {
    let margin = {top: 20, right: 40, bottom: 60, left: 40};

    let height = 400 - margin.bottom - margin.top;
    let width = 960 - margin.right - margin.left

    let svg = container.append("div")
        .classed("graphContainer", true)
        .attr("id", "graphContainer_" + metricID)
        .append("svg")
        .classed("svg-chart", true)
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 960 400")
        .append("g").attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    //Sort points by Data
    dataPoints.sort(function (a, b) {
        return b.values.value - a.values.value;
    });

    let dataCorpusLeft = dataPoints.filter(el => el.corpus == "Corpus1");
    let dataCorpusRight = dataPoints.filter(el => el.corpus == "Corpus2");

    //let sliceEnd = d3.min([dataCorpusLeft.length, dataCorpusRight.length]) < 25 ? d3.min([dataCorpusLeft.length, dataCorpusRight.length]) : 24;

    dataCorpusLeft = dataCorpusLeft.slice(0, 24);
    dataCorpusRight = dataCorpusRight.slice(0, 24);

    dataPoints = dataCorpusLeft.concat(dataCorpusRight);

    //tooltip
    let tooltip = container
        .append("div")
        .style("opacity", 0)
        .classed("tooltip-cust", true)
        .attr("id", metricID + "_tooltip");

    // Color scale
    let myColor = d3.scaleSequential()
        .interpolator(d3.interpolateWarm)
        .domain([0, 2]);

    let mouseover = function (d) {
        d3.select(this).style("stroke-width", "2px");

        tooltip
            .transition()
            .duration(200)
            .style("opacity", 1);
        tooltip
            .html("<span style='color:grey'>Wert: </span>" + d.value + "<span style='color:grey'> Wort: </span>" + d.text + "<span style='color:grey'> Korpus: </span>" + d.corpus);
    };

    let mouseleave = function (d) {
        tooltip
            .transition()
            .duration(200)
            .style("opacity", 0)

        d3.select(this).style("stroke-width", "1px");
    };

    let fontScale = d3.scaleLinear()
        .range([10, 30])
        .domain([dataPoints[dataPoints.length - 1].values.value, dataPoints[0].values.value]);

    let layout = d3.layout.cloud()
        .size([width, height])
        .words(dataPoints.map(function (d) {
            return {text: d.values.name, size: d.values.value, corpus: d.corpus, value: d.values.value}
        }))
        .padding(5)
        .rotate(function () {
            return ~~(Math.random() * 2) * 90;
        })
        .fontSize(function (d) {
            return fontScale(d.size);
        })
        .on("end", draw);

    layout.start();


    function draw(words) {
        svg
            .append("g")
            .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function (d) {
                return d.size;
            })
            .style("fill", function (d) {
                return myColor(d.corpus.substring(6, 7));
            })
            .attr("text-anchor", "middle")
            .style("font-family", "Impact")
            .attr("transform", function (d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function (d) {
                return d.text;
            })
            .on("mouseleave", mouseleave)
            .on("mouseover", mouseover);
    };


}

function createCSVdownload(metricID, dataPoints, section, sectionNum) {

    let metric_name = metricID.split("_")[2]
    let downloadButton = d3.select("#download_" + metric_name);
    downloadButton.style("visibility", "visible");

    let sectionNumCon;
    //catch undefined error
    if (sectionNum != undefined) {
        sectionNumCon = sectionNum === "totals" ? "totals" : parseInt(sectionNum) + 1;
    }
    ;

    let csv_text = convertJSONtoCSV(dataPoints, section, sectionNumCon);

    //Create header for every key
    let csv_header = "";
    for (key of Object.keys(dataPoints[0].values)) {
        if (csv_header != "") {
            csv_header += ", "
        }
        csv_header += key
    }

    //append additional information depending on section or total
    if (section == undefined && sectionNum == undefined) {
        csv_header += ", corpus" + ", variant" + "\r\n";
    } else {
        csv_header += ", corpus" + ", variant" + ", area" + ", areaNum" + "\r\n";
    }

    csv_text = csv_header + csv_text;

    let csv_data = "data:text/plain;charset=utf-8," + encodeURIComponent(csv_text);
    downloadButton.attr("href", csv_data);
    downloadButton.attr("download", metric_name + "_csvdata")

    function convertJSONtoCSV(data, section, sectionNum) {
        let csv_text = "";
        for (let i = 0; i < data.length; i++) {
            let data_row = "";
            for (key of Object.keys(data[i].values)) {
                if (data_row != "") {
                    data_row += ", "
                }
                if (Array.isArray(data[i].values[key])) {
                    data_row += data[i].values[key].join("; ");
                } else {
                    data_row += data[i].values[key];
                }
            }
            //if no textVar selection is available, assume Raw Text
            let textVar = d3.select("#textVar_" + data[i].corpus + "_" + metricID).empty() ? "Raw" : d3.select("#textVar_" + data[i].corpus + "_" + metricID).node().options[d3.select("#textVar_" + data[i].corpus + "_" + metricID).node().selectedIndex].value

            //append data for sectioned metrics
            if (section == undefined && sectionNum == undefined) {
                csv_text += data_row + ", " + data[i].corpus + ", " + textVar + "\r\n";
            } else {
                csv_text += data_row + ", " + data[i].corpus + ", " + textVar + ", " + section + ", " + sectionNum + "\r\n";
            }
            ;
        }
        return csv_text;
    };
};

function createCSVdownloadfromArray(metricID, dataArray) {

    let metric_name = metricID.split("_")[2]
    let downloadButton = d3.select("#download_" + metric_name);
    downloadButton.style("visibility", "visible");

    let csv_text = "";
    let csv_header = "";

    for (element of dataArray) {
        //catch undefined error
        if (element.sectionNum != undefined) {
            sectionNumCon = element.sectionNum === "totals" ? "totals" : parseInt(element.sectionNum) + 1;
        }
        ;

        csv_text += convertJSONtoCSV(element.values, element.section, sectionNumCon, element.corpus);

        //Create header for every key
        if (csv_header === "") {
            for (key of Object.keys(element.values[0])) {
                if (csv_header != "") {
                    csv_header += ", "
                }
                csv_header += key
            }
            ;

            //append additional information depending on section or total
            if (element.section == undefined && element.sectionNum == undefined) {
                csv_header += ", corpus" + ", variant" + "\r\n";
            } else {
                csv_header += ", corpus" + ", variant" + ", area" + ", areaNum" + "\r\n";
            }
            ;
        }
        ;
    }
    ;

    csv_text = csv_header + csv_text;


    let csv_data = "data:text/plain;charset=utf-8," + encodeURIComponent(csv_text);
    downloadButton.attr("href", csv_data);
    downloadButton.attr("download", metric_name + "_csvdata");

    function convertJSONtoCSV(data, section, sectionNum, corpusNum) {
        let csv_text = "";

        for (let i = 0; i < data.length; i++) {
            let data_row = "";
            for (key of Object.keys(data[i])) {
                if (data_row != "") {
                    data_row += ", "
                }
                if (Array.isArray(data[i][key])) {
                    data_row += data[i][key].join("; ");
                } else {
                    data_row += data[i][key];
                }


            }
            //if no textVar selection is available, assume Raw Text
            let textVar = d3.select("#textVar_" + corpusNum + "_" + metricID).empty() ? "Raw" : d3.select("#textVar_" + corpusNum + "_" + metricID).node().options[d3.select("#textVar_" + corpusNum + "_" + metricID).node().selectedIndex].value

            //append data for sectioned metrics
            if (section == undefined && sectionNum == undefined) {
                csv_text += data_row + ", " + corpusNum + ", " + textVar + "\r\n";
            } else {
                csv_text += data_row + ", " + corpusNum + ", " + textVar + ", " + section + ", " + sectionNum + "\r\n";
            }
            ;
        }
        return csv_text;
    };
};

function recalculateMetric(metricID, textVariantKorpus1, textVarianteKorpus2) {
    $.ajax({
        url: calculateURL,
        type: 'GET',
        data: {fieldname: metricID.split('_')[2], Korpus1_variante: textVariantKorpus1, Korpus2_variante: textVarianteKorpus2},
        beforeSend: function () {
            $("#" + metricID).next().children(".indicator").attr("src", "/static/img/results/stopwatch.png");
        },
        success: function (response) {
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
        let graphType = $("#" + metricID).attr("data-graphtype");
        let allowTextVariants = ($("#" + metricID).attr("data-allowTextVariants").toLowerCase() == "true");
        let foundation = $("#" + metricID).attr("data-foundation");

        $("#" + metricID).next().children(".indicator").attr("src", "/static/img/results/verified.png")

        switch (statisticDisplayType) {
            case "numeric-total":
                returnGraphNumericTotal(metricID, collapseEl, data, textVariants, graphType, allowTextVariants);
                break;
            case "numeric-section":
                returnGraphNumericSection(metricID, collapseEl, data, textVariants, graphType, allowTextVariants);
                break;
            case "text-total":
                returnGraphTextTotal(metricID, collapseEl, data, textVariants, graphType, allowTextVariants, foundation)
                break;
            case "text-section":
                break;
        }

    }
}

function createStatElement(container, mod, med, avg, std, cnt) {

    container.append("p").classed("metric-statdata", true).attr("data-tooltip", "Modus: Der häufigste Wert").html("<span class='metric-prefix'>Mod:</span>" + mod);
    container.append("p").classed("metric-statdata", true).attr("data-tooltip", "Median: Der Zentralwert").html("<span class='metric-prefix'>Med:</span>" + med);
    container.append("p").classed("metric-statdata", true).attr("data-tooltip", "Durchschnitt: Der Mittelwert").html("<span class='metric-prefix'>Avg:</span>" + avg);
    container.append("p").classed("metric-statdata", true).attr("data-tooltip", "Standardabweichung: Mittlere Abweichung der Streuung").html("<span class='metric-prefix'>Std:</span>" + std);
    container.append("p").classed("metric-statdata", true).attr("data-tooltip", "Anzahl der betrachteten Dokumente").html("<span class='metric-prefix'>Cnt:</span>" + cnt);

}

function drawGraph(IDMetricEl, metricContainer, calcStatisticalData, calcRawData, graphType) {

    switch (graphType) {
        case "boxplot":
            drawBoxplotGraph(IDMetricEl, metricContainer, calcStatisticalData, calcRawData);
            break;
        case "lollipop":
            if (calcStatisticalData.length == 2) {
                drawDoubleLollipopGraph(IDMetricEl, metricContainer, calcStatisticalData, calcRawData);
            }
            ;

            if (calcStatisticalData.length == 1) {
                drawLollipopGraph(IDMetricEl, metricContainer, calcStatisticalData, calcRawData);
            }
            ;
            break;
        case "wordcloud":
            drawWordCloudGraph(IDMetricEl, metricContainer, calcStatisticalData, calcRawData);
            break;
    }
    ;

};


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

function convertDataSectionNumericStatistics(data, metricName, section, sectionNum) {
    statisticsArr = []
    for (corpus in data[metricName]) {
        if (sectionNum === "totals") {
            statisticsArr.push({"corpus": corpus, "value": data[metricName][corpus].statisticalValues.totals[section]});
        } else {
            statisticsArr.push({"corpus": corpus, "value": data[metricName][corpus].statisticalValues.sectioned[section][parseInt(sectionNum)]});
        }
        ;
    }
    ;
    return statisticsArr;
};

function convertDataSectionNumericRawValues(data, metricName, section, sectionNum) {
    let rawValuesArr = [];
    for (corpus in data[metricName]) {
        if (sectionNum === "totals") {
            for (entry of data[metricName][corpus].rawValues.totals[section]) {
                rawValuesArr.push({"corpus": corpus, "values": entry});
            }
            ;

        } else {
            for (entry of data[metricName][corpus].rawValues.sectioned[section][parseInt(sectionNum)]) {
                rawValuesArr.push({"corpus": corpus, "values": entry});
            }
            ;
        }
    }
    ;
    return rawValuesArr;
}


