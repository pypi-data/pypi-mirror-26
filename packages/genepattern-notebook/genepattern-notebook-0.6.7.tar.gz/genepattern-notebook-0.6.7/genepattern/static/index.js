/**
 * @author Thorin Tabor
 *
 * Loads the GenePattern Notebook extension for Jupyter Notebook
 *
 * Copyright 2015-2016 The Broad Institute, Inc.
 *
 * SOFTWARE COPYRIGHT NOTICE
 * This software and its documentation are the copyright of the Broad Institute, Inc. All rights are reserved.
 * This software is supplied without any warranty or guaranteed support whatsoever. The Broad Institute is not
 * responsible for its use, misuse, or functionality.
 */

define([
    // Load the dependencies
    "base/js/namespace", "base/js/events", "jquery",

    // Bootstrap loading the GenePattern requirejs modules
    "nbextensions/genepattern/resources/gp",
    "nbextensions/genepattern/resources/navigation",
    "nbextensions/genepattern/resources/auth-widget",
    "nbextensions/genepattern/resources/job-widget",
    "nbextensions/genepattern/resources/task-widget",
    "nbextensions/genepattern/resources/ui-builder"], function(Jupyter, events, $) {

    function load_ipython_extension() {
        var STATIC_PATH = Jupyter.notebook.base_url + "nbextensions/genepattern/resources/";

        $('head')
            // Import styles used by GenePattern navigation
            .append(
                $('<link rel="stylesheet" type="text/css" />')
                    .attr("rel", "stylesheet")
                    .attr("type", "text/css")
                    .attr('href', STATIC_PATH + 'navigation.css')
            )
            // Import styles used by GenePattern widgets
            .append(
                $('<link rel="stylesheet" type="text/css" />')
                    .attr("rel", "stylesheet")
                    .attr("type", "text/css")
                    .attr('href', STATIC_PATH + 'widget.css')
            );

        // Wait for the kernel to be ready and then initialize the widgets
        require(["genepattern/navigation"], function(GPNotebook) {
            var interval = setInterval(function() {
                GPNotebook.init.wait_for_kernel(interval);
            }, 500);
        });
    }

    return {
        load_ipython_extension: load_ipython_extension
    };
});