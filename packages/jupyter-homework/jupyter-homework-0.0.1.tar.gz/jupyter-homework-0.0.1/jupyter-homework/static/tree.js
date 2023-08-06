define(function() {
  return {
    load_ipython_extension: function() {
      require(['nbextensions/jupyter-homework/common'], function(homework) {
        homework.attach_menu('tree', function(menu) {
          var title = $('<button/>')
            .addClass('dropdown-toggle btn btn-default btn-xs')
            .attr('data-toggle', 'dropdown')
            .append($('<span/>').text("Homework "))
            .append($('<span/>').addClass("caret"));

          var dropdown = $('<div/>')
            .addClass('btn-group')
            .append(title)
            .append(menu);

          $('.tree-buttons .pull-right').prepend(dropdown);
        });
      });
    }
  }
});
