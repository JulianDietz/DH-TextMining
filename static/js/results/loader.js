$(document).ready(function () {
    $(".toggle_button").click(function () {

        const textVariants = [{"key": "orig", "value": "Raw", "display": "Original"},
            {"key": "stpw", "value": "NltkStw", "display": "Stopwortgefiltert"},
            {"key": "stmd", "value": "NltkStem", "display": "Gestemmt"}];

        let $this = $(this);
        console.log($this);

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
    let metricName = IDMetricEl.split("_")[2];

    //Section selector
    let metricSectionSelectorContainer = d3.select(htmlEl[0]).append("div").classed("metricSectionSelectorContainer", true).attr("id", "metricSectionSelectorContainer_" + IDMetricEl);

    metricSectionSelectorContainer.append("p").text("Abschnitt:").style("display", "inline-block");
    let sectionSelector = metricSectionSelectorContainer.append("select").classed("paperAreaSelector", true);

    for (area in data[metricName].Corpus1.rawValues.totals) {
        //TODO debug
        //if (area != "titles") {
        sectionSelector.append("option").attr("value", area).text(area);
        //};
    }
    ;

    sectionSelector.on("change", function () {
        d3.select("#metricDescription_" + IDMetricEl).remove();
        d3.select("#graphContainer_" + IDMetricEl).remove();
        d3.select("#" + IDMetricEl + "_tooltip").remove();


        drawInfo();
    });

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

        //header and Total
        for (corpus in data[metricName]) {
            tableHeader.append("th").text(corpus);

            let cell = tableTotalRow.append("td")
            let mode = data[metricName][corpus].statisticalValues.totals[areaSelected].mode != undefined ? data[metricName][corpus].statisticalValues.totals[areaSelected].mode.join(", ") : "-";
            let med = data[metricName][corpus].statisticalValues.totals[areaSelected].median != undefined ? data[metricName][corpus].statisticalValues.totals[areaSelected].median.toFixed(2) : "-";
            let avg = data[metricName][corpus].statisticalValues.totals[areaSelected].average != undefined ? data[metricName][corpus].statisticalValues.totals[areaSelected].average.toFixed(2) : "-";
            let variance = data[metricName][corpus].statisticalValues.totals[areaSelected].variance != undefined ? data[metricName][corpus].statisticalValues.totals[areaSelected].variance.toFixed(2) : "-";

            cell.append("p").classed("metric-data modus-text", true).text(mode).attr("data-before", "Modus: ");
            cell.append("p").classed("metric-data median-text", true).text(med).attr("data-before", "Median: ");
            cell.append("p").classed("metric-data average-text", true).text(avg).attr("data-before", "Durchschnitt: ");
            cell.append("p").classed("metric-data variance-text", true).text(variance).attr("data-before", "Varianz: ");
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
                let mode = data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].mode != undefined ? data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].mode.join(", ") : "-";
                let med = data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].median != undefined ? data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].median.toFixed(2) : "-";
                let avg = data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].average != undefined ? data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].average.toFixed(2) : "-";
                let variance = data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].variance != undefined ? data[metricName][corpus].statisticalValues.sectioned[areaSelected][area].variance.toFixed(2) : "-";

                cell.append("p").classed("metric-data modus-text", true).text(mode).attr("data-before", "Modus: ");
                cell.append("p").classed("metric-data median-text", true).text(med).attr("data-before", "Median: ");
                cell.append("p").classed("metric-data average-text", true).text(avg).attr("data-before", "Durchschnitt: ");
                cell.append("p").classed("metric-data variance-text", true).text(variance).attr("data-before", "Varianz: ");

            }
            ;
        }
        ;

        function updateGraph(section, sectionNum) {

            d3.select("#graphContainer_" + IDMetricEl).remove();
            d3.select("#" + IDMetricEl + "_tooltip").remove();

            let calcRawData = convertDataSectionNumericRawValues(data, metricName, section, sectionNum);
            let calcStatisticalData = convertDataSectionNumericStatistics(data, metricName, section, sectionNum);

            //NEU ENDE
            //draw the boxplot
            drawBoxplot(IDMetricEl, metricContainer, calcStatisticalData, calcRawData);

            //Create CSV file and download
            createCSVdownload(IDMetricEl, calcRawData, section, sectionNum);

        }


    };
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
        d3.select(this).style("stroke-width", "2px");

        tooltip
            .transition()
            .duration(200)
            .style("opacity", 1);
        tooltip
            .html("<span style='color:grey'>Wert: </span>" + d.values.value + "<span style='color:grey'> Titel: </span>" + d.values.paperTitle + " (" + d.values.year + ") " + d.values.authors[0]);
    };
    let mouseleave = function (d) {
        tooltip
            .transition()
            .duration(200)
            .style("opacity", 0)

        d3.select(this).style("stroke-width", "1px");
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

function createCSVdownload(metricID, dataPoints, section, sectionNum) {

    let metric_name = metricID.split("_")[2]
    let downloadButton = d3.select("#download_" + metric_name);
    downloadButton.style("visibility", "visible");

    let sectionNumCon = sectionNum === "totals" ? "totals" : parseInt(sectionNum) + 1;

    let csv_text = convertJSONtoCSV(dataPoints, section, sectionNumCon);

    let csv_header = "";
    for (key of Object.keys(dataPoints[0].values)) {
        if (csv_header != "") {
            csv_header += ", "
        }
        csv_header += key
    }

    console.log(section, sectionNum);

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
            for (key of Object.keys(dataPoints[i].values)) {
                if (data_row != "") {
                    data_row += ", "
                }
                if (Array.isArray(dataPoints[i].values[key])) {
                    data_row += dataPoints[i].values[key].join(";");
                } else {
                    data_row += dataPoints[i].values[key];
                }


            }
            console.log("#textVar_" + dataPoints[i].corpus.toString() + "_" + metricID);
            let textVar = d3.select("#textVar_" + dataPoints[i].corpus + "_" + metricID).node().options[d3.select("#textVar_" + dataPoints[i].corpus + "_" + metricID).node().selectedIndex].value

            csv_text += data_row + ", " + dataPoints[i].corpus + ", " + textVar + ", " + section + ", " + sectionNum + "\r\n";
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
            $("#collapse_button_" + metricID).next().children(".indicator").attr("src", "/static/img/results/stopwatch.png");
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

        $("#" + metricID).next().children(".indicator").attr("src", "/static/img/results/verified.png")

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


