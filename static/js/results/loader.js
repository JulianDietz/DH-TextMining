$(document).ready(function () {
    $(".toggle_button").click(function () {

        let $this = $(this);
        let collapseEl = $($this.attr("data-collapse"));


        if ($this.attr("data-ready") == "false") {
            setTimeout(function () {

                returnGraph($this.attr("id"), collapseEl, null);

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


function returnGraph(name, htmlEl, data2, data1) {

    var sumstat = [{"key": "Korpus 1", "value": {"q1": 4.8, "median": 5, "q3": 5.2, "interQuantileRange": 0.40000000000000036, "min": 4.199999999999999, "max": 5.800000000000001}}, {
        "key": "Korpus 2",
        "value": {"q1": 5.6, "median": 5.9, "q3": 6.3, "interQuantileRange": 0.7000000000000002, "min": 4.549999999999999, "max": 7.35}
    }];

    let data = sumstat;

    let metricContainer = d3.select(htmlEl[0]);

    let metricDescription = metricContainer.append("div").classed("metricDescription", true).classed("row", true);

    let metricDescriptionCol = metricDescription.append("div").classed("col", true).attr("style", "display: inline-block;");

    metricDescriptionCol.append("div").classed("metricDescriptionColHeader", true).text("Korpus 1");
    let metricDescriptionTags = metricDescriptionCol.append("div").classed("metricDescriptionColTags", true);

    metricDescriptionTags.append("p").classed("metric-data median-text", true).text(data[0].value.median).attr("data-before", "Median: ");
    metricDescriptionTags.append("p").classed("metric-data average-text", true).text(data[0].value.q3).attr("data-before", "Durchschnitt: ");
    metricDescriptionTags.append("p").classed("metric-data variance-text", true).text(data[0].value.interQuantileRange.toFixed(2)).attr("data-before", "Varianz: ");
    metricDescriptionTags.append("p").classed("metric-data modus-text", true).text(data[0].value.max.toFixed(2)).attr("data-before", "Modus: ");

    if (data[1].key == "Korpus 2") {

        let metricDescriptionCol2 = metricDescription.append("div").classed("col", true).attr("style", "display: inline-block;");

        metricDescriptionCol2.append("div").classed("metricDescriptionColHeader", true).text("Korpus 2");
        let metricDescriptionTags2 = metricDescriptionCol2.append("div").classed("metricDescriptionColTags", true);

        metricDescriptionTags2.append("p").classed("metric-data median-text", true).text(data[1].value.median).attr("data-before", "Median: ");
        metricDescriptionTags2.append("p").classed("metric-data average-text", true).text(data[1].value.q3).attr("data-before", "Durchschnitt: ");
        metricDescriptionTags2.append("p").classed("metric-data variance-text", true).text(data[1].value.interQuantileRange.toFixed(2)).attr("data-before", "Varianz: ");
        metricDescriptionTags2.append("p").classed("metric-data modus-text", true).text(data[1].value.max.toFixed(2)).attr("data-before", "Modus: ");

    }

    var margin = {top: 20, right: 40, bottom: 60, left: 120};

    let height = 200 - margin.bottom - margin.top;
    let width = 960 - margin.right - margin.left;

    let svg = metricContainer.append("div")
        .classed("graphContainer", true)
        .append("svg")
        .classed("svg-chart", true)
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 960 200")
        .append("g").attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

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
        .data(sumstat)
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
        .data(sumstat)
        .enter()
        .append("rect")
        .attr("x", function (d) {
            return (x(d.value.q1))
        }) // console.log(x(d.value.q1)) ;
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
        .data(sumstat)
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


    let dataPoints = JSON.parse('[{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"4.9","corpus":"Korpus 2"},{"metric_value":"4.7","corpus":"Korpus 2"},{"metric_value":"4.6","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"5.4","corpus":"Korpus 2"},{"metric_value":"4.6","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"4.4","corpus":"Korpus 2"},{"metric_value":"4.9","corpus":"Korpus 2"},{"metric_value":"5.4","corpus":"Korpus 2"},{"metric_value":"4.8","corpus":"Korpus 2"},{"metric_value":"4.8","corpus":"Korpus 2"},{"metric_value":"4.3","corpus":"Korpus 2"},{"metric_value":"5.8","corpus":"Korpus 2"},{"metric_value":"5.7","corpus":"Korpus 2"},{"metric_value":"5.4","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"5.7","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"5.4","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"4.6","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"4.8","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"5.2","corpus":"Korpus 2"},{"metric_value":"5.2","corpus":"Korpus 2"},{"metric_value":"4.7","corpus":"Korpus 2"},{"metric_value":"4.8","corpus":"Korpus 2"},{"metric_value":"5.4","corpus":"Korpus 2"},{"metric_value":"5.2","corpus":"Korpus 2"},{"metric_value":"5.5","corpus":"Korpus 2"},{"metric_value":"4.9","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"5.5","corpus":"Korpus 2"},{"metric_value":"4.9","corpus":"Korpus 2"},{"metric_value":"4.4","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"4.5","corpus":"Korpus 2"},{"metric_value":"4.4","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"4.8","corpus":"Korpus 2"},{"metric_value":"5.1","corpus":"Korpus 2"},{"metric_value":"4.6","corpus":"Korpus 2"},{"metric_value":"5.3","corpus":"Korpus 2"},{"metric_value":"5","corpus":"Korpus 2"},{"metric_value":"7","corpus":"Korpus 1"},{"metric_value":"6.4","corpus":"Korpus 1"},{"metric_value":"6.9","corpus":"Korpus 1"},{"metric_value":"5.5","corpus":"Korpus 1"},{"metric_value":"6.5","corpus":"Korpus 1"},{"metric_value":"5.7","corpus":"Korpus 1"},{"metric_value":"6.3","corpus":"Korpus 1"},{"metric_value":"4.9","corpus":"Korpus 1"},{"metric_value":"6.6","corpus":"Korpus 1"},{"metric_value":"5.2","corpus":"Korpus 1"},{"metric_value":"5","corpus":"Korpus 1"},{"metric_value":"5.9","corpus":"Korpus 1"},{"metric_value":"6","corpus":"Korpus 1"},{"metric_value":"6.1","corpus":"Korpus 1"},{"metric_value":"5.6","corpus":"Korpus 1"},{"metric_value":"6.7","corpus":"Korpus 1"},{"metric_value":"5.6","corpus":"Korpus 1"},{"metric_value":"5.8","corpus":"Korpus 1"},{"metric_value":"6.2","corpus":"Korpus 1"},{"metric_value":"5.6","corpus":"Korpus 1"},{"metric_value":"5.9","corpus":"Korpus 1"},{"metric_value":"6.1","corpus":"Korpus 1"},{"metric_value":"6.3","corpus":"Korpus 1"},{"metric_value":"6.1","corpus":"Korpus 1"},{"metric_value":"6.4","corpus":"Korpus 1"},{"metric_value":"6.6","corpus":"Korpus 1"},{"metric_value":"6.8","corpus":"Korpus 1"},{"metric_value":"6.7","corpus":"Korpus 1"},{"metric_value":"6","corpus":"Korpus 1"},{"metric_value":"5.7","corpus":"Korpus 1"},{"metric_value":"5.5","corpus":"Korpus 1"},{"metric_value":"5.5","corpus":"Korpus 1"},{"metric_value":"5.8","corpus":"Korpus 1"},{"metric_value":"6","corpus":"Korpus 1"},{"metric_value":"5.4","corpus":"Korpus 1"},{"metric_value":"6","corpus":"Korpus 1"},{"metric_value":"6.7","corpus":"Korpus 1"},{"metric_value":"6.3","corpus":"Korpus 1"},{"metric_value":"5.6","corpus":"Korpus 1"},{"metric_value":"5.5","corpus":"Korpus 1"},{"metric_value":"5.5","corpus":"Korpus 1"},{"metric_value":"6.1","corpus":"Korpus 1"},{"metric_value":"5.8","corpus":"Korpus 1"},{"metric_value":"5","corpus":"Korpus 1"},{"metric_value":"5.6","corpus":"Korpus 1"},{"metric_value":"5.7","corpus":"Korpus 1"},{"metric_value":"5.7","corpus":"Korpus 1"},{"metric_value":"6.2","corpus":"Korpus 1"},{"metric_value":"5.1","corpus":"Korpus 1"},{"metric_value":"5.7","corpus":"Korpus 1"}]');

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


    let metric_name = name.split("_")[2]
    let downloadButton = d3.select("#download_" + metric_name;
    downloadButton.style("visibility", "visible");

    let csv_text = convertJSONtoCSV(dataPoints);

    //add CSV header
    csv_text = metric_name +  "_values," + "corpus" + "\r\n" + csv_text;


    let csv_data = "data:text/plain;charset=utf-8," + encodeURIComponent(csv_text);
    downloadButton.attr("href", csv_data);
    downloadButton.attr("download", metric_name + "_csvdata");

};

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
}


