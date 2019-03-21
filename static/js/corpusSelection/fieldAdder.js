$(document).ready(function () {

    addCorpusSelection(1);

    //        {"key": "", "value" : "", "display": ""},]

    const addCorpusButton = d3.select("#addCorpusButton").on("click", function () {
        let corpusCount = d3.selectAll(".corpusSelectionContainer").size();

        //add corpus
        if (corpusCount < 2) {
            d3.select(this).text("-");
            addCorpusSelection(corpusCount + 1);
            //remove corpus
        } else {
            d3.select(this).text("+");
            removeCorpusSelection(corpusCount);
        }
        ;
    });


})

function addCorpusSelection(corpusID) {
    let corpusContainer = d3.select("#container")
        .append("div")
        .classed("corpusSelectionContainer", true)
        .attr("id", "corpus_" + corpusID);

    //Header
    corpusContainer.append("h3")
        .text("Korpus " + corpusID)
        .classed("corpusSelectionHeader", true);

    //Field-Adder
    corpusContainer.append("div")
        .classed("addSearchDataFieldButton searchDataSelector cust_button", true)
        .attr("id", "corpusFieldAdder_" + corpusID)
        .attr("data-numOfFields", 0)
        .on("click", function () {
            addSelector(corpusContainer, corpusID);
        })
        .append("p")
        .text("Suchfeld hinzufügen")
        .classed("addSearchDataFieldButtonText", true);

    //add first Selector
    addSelector(corpusContainer, corpusID);
};

function removeCorpusSelection(corpusID) {
    d3.select("#corpus_" + corpusID).remove();

};

function addSelector(element, corpusID) {
    const metadataTags = [{"key": "authors", "value": "authors", "display": "Autoren"},
        {"key": "year", "value": "yearOfArticle", "display": "Jahr"},
        {"key": "source", "value": "source", "display": "Quelle"},
        {"key": "journal", "value": "journal", "display": "Journal"},
        {"key": "keywords", "value": "keywords", "display": "Keywords"},
        {"key": "organization", "value": "organization", "display": "Organisation"},
        {"key": "Category", "value": "category", "display": "Kategorie"},
        {"key": "language", "value": "language", "display": "Sprache"},
        {"key": "title", "value": "title", "display": "Titel"}];

    let numDataSelector = parseInt(d3.select("#corpusFieldAdder_" + corpusID).attr("data-numOfFields"));
    numDataSelector += 1;
    d3.select("#corpusFieldAdder_" + corpusID)
        .attr("data-numOfFields", numDataSelector);


    //Container element
    let searchDataSelector = element
        .insert("div", ":nth-Child(2)")
        .classed("searchDataSelector", true)
        .attr("name", "dataselector_" + numDataSelector);

    //Select field
    let selectSearchDataFieldSelect = searchDataSelector
        .append("select")
        .classed("selectSearchDataFieldSelect", true)
        .attr("name", "optionfield_" + numDataSelector + "_CorpusID_" + corpusID);

    //Select-Optionen
    selectSearchDataFieldSelect
        .selectAll("option")
        .data(metadataTags)
        .enter()
        .append("option")
        .attr("value", function (d) {
            return d.value
        })
        .text(function (d) {
            return d.display
        })
        .attr("name", "optionField_" + numDataSelector);

    //Inputfield
    searchDataSelector.append("input").classed("searchDataUserInput", true)
        .attr("name", "inputfield_" + numDataSelector + "_CorpusID_" + corpusID)
        .attr("type", "text");

    //Remove button
    searchDataSelector.append("div").classed("removeSearchDataFieldButton", true).text("-").on("click", function () {
        d3.select(this.parentNode).transition().style("opacity", 0).remove();
    });
};