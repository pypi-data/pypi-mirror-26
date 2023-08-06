define(function() {
  var config = function(callback) {
    require(['base/js/utils','services/config'], function(utils,configmod) {
      var conf = new configmod.ConfigSection('common',{base_url: utils.get_body_data("baseUrl")});
      conf.load();
    
      conf.loaded.then(function() {
        var homework = conf['data'].homework;

        if (homework == undefined) {
          homework = {url:'http://localhost:5953'}
          conf.update({homework:homework});
        }
        
        callback(conf);
      });
    });
  };

  var hook = function(script,success=function(){},failure=function(){}) {
    config(function(conf) {
      var path = conf['data'].homework.url + "/" + script + ".js";
      console.log("homework extension: loading " + path);
      require([path],success,failure);
    });
  };

  var attach_menu = function(script,callback) {
    config(function(conf) {
      require(['nbextensions/jupyter-homework/bootbox.min'], function(bootbox) {
        var configure = $('<li/>')
          .append(
            $('<a/>')
              .attr('href','#')
              .text('Configure...')
              .click(function() {
                bootbox.prompt({
                  title: 'Homework Server Address',
                  value: conf['data'].homework.url,
                  callback: function (result) {
                    if (result != null) {
                      conf['data'].homework.url = result;
                      conf.update({homework:conf['data'].homework});
                    }
                  }
                });
              })
          );

        var message = $('<a/>')
          .attr('href','#')
          .addClass('message')
          .text('Connecting to homework server ...');

        var status = $('<li/>')
          .addClass('disabled')
          .attr('id','hwStatus')
          .append(message);

        var menu = $('<ul/>')
          .attr('id','#hwMenu')
          .addClass('dropdown-menu')
          .append(configure)
          .append(status);

        callback(menu);

        hook(script, 
          function() {
            $('#hwStatus').remove();
          },function() {
            $('#hwStatus .message')
              .addClass('alert-danger')
              .text('Homework server unreachable')
          });
      });
    });
  };

  return {
    hook: hook,
    config: config,
    attach_menu: attach_menu,
    load_ipython_extension: hook('common')
  }
});