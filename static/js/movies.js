function forEach(array, action) {
  for (var i = 0; i < array.length; i++)
  action(array[i]);
}

function addRow(){
    var editableContent = $('#moviesTable').find('tr .editable');
    if (editableContent.length){
      logMessage('Save the row before proceeding');
      return;
    }

    var clonedRow = $('#moviesTable').children().children()[1];
    clonedRow = $(clonedRow).clone();
    $(clonedRow).find('td[data-type]').text('');
    $('#moviesTable').append(clonedRow);
    var rowElements = $(clonedRow).find('td[data-type]');
    editingRowsDone(rowElements);
  }

function editRow(element) {
    var row = $(element).closest('tr');
    var rowElements = $(row).find('td[data-type]');
    var done = editingRowsDone(rowElements);
    if (done){
      submitMovie(rowElements);
    }
  }

function editingRowsDone(rowElements){
    // clear warning messages, if any
    logMessage('');

    var rowEditable = $(rowElements).is('.editable');
    $(rowElements).prop('contenteditable',!rowEditable).toggleClass('editable');

    var button = $(rowElements).parent().find('a');
    if (button.text() === 'Edit'){
      $(button).text('Done');
      $(button).addClass('green');
    }
    else{
      $(button).text('Edit');
      $(button).removeClass('green');
    }
    return rowEditable;
}


function submitMovie(rowElements){
    // read off values for the current movie
    var movieData = {};
    forEach(rowElements, function (el) {
      debugger
      movieData[$(el).attr('data-type')] = $(el).text();
    });
    movieData = JSON.stringify(movieData);
    
    console.log(movieData);
  

    $.ajax({
      url: '/movies/api/v1.0/edit',
      data: movieData,
      type: 'POST',
      contentType:'application/json',
      context: rowElements,
      success: function(data){
        var _rowElements = this;
        var _data = data['movie'];
        console.log(_data);
        forEach(_rowElements, function (el) {
          $(el).text(_data[$(el).attr('data-type')]);
        });

      },
      error: function() {
        logMessage('Error occurred');
      }

    });
  }

function logMessage(message){
  $("#errorDiv").fadeOut(function() {
    $("#errorDiv").text(message).fadeIn();
  });
}
