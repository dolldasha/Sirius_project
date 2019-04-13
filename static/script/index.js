let sensors_mark = [];

function getData() {
    setInterval(function () {
        $.ajax({
            url: '/api/values',
            method: 'GET',
            success: function (data) {
                data = JSON.parse(data);
                console.log(data);
                // sensors.
                let sensors = data['sensors'];
                for (let i = 0; i < sensors.length; i++) {
                    let sensor = sensors[i];
                    console.log(sensor['id']);
                    if (sensors_mark.includes(sensor['id']) === false) {
                        sensors_mark.push(sensor['id']);
                        $('.block').append('<div class="sensor-block ' + sensor['id'] + '">\n' +
                            '        <div class="sensor-name">\n' +
                            '            #NAME\n' +
                            '        </div>\n' +
                            '        <div class="sensor-values">\n' +
                            '            #VALUE\n' +
                            '        </div>\n' +
                            '        <div class="sensor-status">\n' +
                            '            #STATUS\n' +
                            '        </div>\n' +
                            '    </div>');
                    }
                    let div_class = '.' + sensor['id'];
                    $(div_class + ' .sensor-name').text(sensor['name']);
                    $(div_class + ' .sensor-values').text(sensor['value']);
                    $(div_class + ' .sensor-name').text(sensor['name']);
                }
            }
        });
    }, 1000);
}

$(document).ready(function () {
    getData();
});