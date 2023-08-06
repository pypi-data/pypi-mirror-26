define(function() {
  return {
    load_ipython_extension: function() {
      require(['nbextensions/jupyter-homework/common'], function(homework) {
        homework.attach_menu('notebook', function(menu) {
          var title = $('<a/>')
            .text('Homework')
            .attr('href','#')
            .addClass('dropdown-toggle')
            .attr('data-toggle', 'dropdown');

          var dropdown = $('<li/>')
            .addClass('dropdown')
            .append(title)
            .append(menu);

          $('.navbar-nav').append(dropdown);
        });
      });
    }
  };
});
