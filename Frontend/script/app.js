const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
var setTemperature, setHumidity, setSoilMoisture, setEco2;

const drawChart = function (labels, data) {
  var options = {
      chart: {
          id: 'sensorChart',
          type: 'line',
      },
      stroke: {
          curve: 'smooth',
      },
      dataLabels: {
          enabled: false,
      },
      series: [
          {
              name: 'Sensor Chart',
              data: data,
          },
      ],
      lables: labels,
      noData: {
          text: 'Loading...',
      },
      colors:['#ADC178'],
  };
  var chart = new ApexCharts(document.querySelector('.js-chart'), options);
  chart.render();
};

const toggleNav = function() {
  let toggleTrigger = document.querySelectorAll(".js-toggle-nav");
  for (let i = 0; i < toggleTrigger.length; i++) {
      toggleTrigger[i].addEventListener("click", function() {
          document.querySelector("body").classList.toggle("has-mobile-nav");
      })
  }
}

const colorIcon = function(sensor, color) {
  document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--grey');
  if (color == 'bright-green') {
    document.querySelector(`.js-icon-box-${sensor}`).classList.add('c-icon-box--bright-green');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--light-green');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--yellow');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--orange');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--red');
  }
  else if (color == 'light-green') {
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--bright-green');
    document.querySelector(`.js-icon-box-${sensor}`).classList.add('c-icon-box--light-green');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--yellow');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--orange');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--red');
  }
  else if (color == 'yellow') {
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--bright-green');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--light-green');
    document.querySelector(`.js-icon-box-${sensor}`).classList.add('c-icon-box--yellow');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--orange');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--red');
  }
  else if (color == 'orange') {
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--bright-green');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--light-green');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--yellow');
    document.querySelector(`.js-icon-box-${sensor}`).classList.add('c-icon-box--orange');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--red');
  }
  else if (color == 'red') {
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--bright-green');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--light-green');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--yellow');
    document.querySelector(`.js-icon-box-${sensor}`).classList.remove('c-icon-box--orange');
    document.querySelector(`.js-icon-box-${sensor}`).classList.add('c-icon-box--red');
  }
}

//#region ***  DOM references                           ***********
let htmlIndex, htmlHistory, htmlSettings;
//#endregion

//#region ***  Callback-Visualisation - show___         ***********
const showMeasurementsDates = function (jsonObject) {
  console.log(jsonObject);
  let converted_labels = [];
  let converted_data = [];
  const htmlMeasurements = document.querySelector('.js-measurements');
    let myInnerHTML = '<table class="c-table"><tr class="c-table-row"><th class="c-table-cell--header">Date and time</th><th class="c-table-cell--header">Measurement</th></tr>';
    for (let data of jsonObject.measurements) {
      myInnerHTML += `<tr class="c-table-row">
      <td class="c-table-cell">${data.Date}</td>
      <td class="c-table-cell">${data.Value} ${data.Unit == null ? ' ' : data.Unit}</td>
      </tr>`;
      converted_labels.push(data.Date);
      converted_data.push(data.Value);
    };
    myInnerHTML += '</table>';
    htmlMeasurements.innerHTML = myInnerHTML;
    drawChart(converted_labels, converted_data);
}

const showSensors = function(jsonObject) {
  let mijnInnerHTML = '';
  for (let sensor of jsonObject.sensors){
    mijnInnerHTML += `<option value="${sensor.DeviceID}">${sensor.Name}</option>`;
  }
  document.querySelector('.js-select-data').innerHTML += mijnInnerHTML;

  //Show data sensor
  // document.querySelector('.js-select-data').addEventListener('input', function () {
  //   let id = this.value;
  //   let date1 = document.querySelector('.js-select-date1').value;
  //   let date2 = document.querySelector('.js-select-date2').value;
  //   getMeasurementsDates(id, date1, date2);
  // });
}

const showDates = function(jsonObject) {
  let mijnInnerHTML1 = '';
  for (let date of jsonObject.dates){
    mijnInnerHTML1 += `<option value="${date.DateFormat}">${date.Date}</option>`;
  }
  document.querySelector('.js-select-date1').innerHTML += mijnInnerHTML1;

  //Show dates after first date sensor
  document.querySelector('.js-select-date1').addEventListener('input', function () {
    let date1 = this.value;
    let mijnInnerHTML2 = '';
    for (let date of jsonObject.dates){
      if (date.DateFormat >= date1) {
        mijnInnerHTML2 += `<option value="${date.DateFormat}">${date.Date}</option>`;
      }
    }
    document.querySelector('.js-select-date2').innerHTML = mijnInnerHTML2;
  });

  // document.querySelector('.js-select-date2').addEventListener('input', function () {
  //   let id = document.querySelector('.js-select-data').value;
  //   let date1 = document.querySelector('.js-select-date1').value;
  //   let date2 = this.value;
  //   getMeasurementsDates(id, date1, date2);
  // });
}

const showTimeWatered = function (jsonObject) {
  document.querySelector('.js-watered').innerHTML = jsonObject.Date;
}

const showStateWindows = function (jsonObject) {
  let myInnerHTML1 = '';
  let myInnerHTML2 = '';
  if (jsonObject.ActionID == 5) {
    myInnerHTML1 = 'CLOSED';
    myInnerHTML2 = 'Open windows';
  }
  else {
    myInnerHTML1 = 'OPEN';
    myInnerHTML2 = 'Close windows';
  }
  document.querySelector('.js-windows').innerHTML = myInnerHTML1;
  document.querySelector('.js-windows-btn').innerHTML = myInnerHTML2;
}

const showSettings = function (jsonObject) {
  if (htmlSettings) {
    console.log(jsonObject);
    let inputs_settings = [document.querySelector('.js-temp'), document.querySelector('.js-humidity'), document.querySelector('.js-soil-moisture'), document.querySelector('.js-co2')]
    for (let setting of jsonObject.settings) {
      for (let input of inputs_settings) {
        if (input.getAttribute('data-typeid') == setting.DeviceID) {
          input.value = setting.Value;
        }
      }
    }
  }
  if (htmlIndex) {
    for (let setting of jsonObject.settings) {
      if (setting.DeviceID == 3) {
        setTemperature = setting.Value;
      }
      else if (setting.DeviceID == 4) {
        setHumidity = setting.Value;
      }
      else if (setting.DeviceID == 1) {
        setSoilMoisture = setting.Value;
      }
      else if (setting.DeviceID == 5) {
        setEco2 = setting.Value;
      }
    }
  }
}

const showStartupTime = function(jsonObject) {
  document.querySelector('.js-startup').innerHTML = jsonObject.Date;
}
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***********
const callbackSaveChanges = function (data) {
  console.log(data);
  document.querySelector('.js-saved').innerHTML = 'Settings saved succesfully';
}
//#endregion

// #region ***  Data Access - get___                     ***********
// const getMeasurementsDates = function(deviceid, date1, date2) {
//   handleData(`http://${lanIP}/api/v1/measurements/${deviceid}/${date1}/${date2}`, showMeasurementsDates);
// }

const getSensors = function () {
  handleData(`http://${lanIP}/api/v1/sensors`, showSensors);
}

const getDates = function () {
  handleData(`http://${lanIP}/api/v1/dates`, showDates);
}

const getTimeWatered = function () {
  handleData(`http://${lanIP}/api/v1/watered`, showTimeWatered);
}

const getStateWindows = function () {
  handleData(`http://${lanIP}/api/v1/windows`, showStateWindows);
}

const getSettings = function () {
  handleData(`http://${lanIP}/api/v1/settings`, showSettings);
}

const getStartupTime = function () {
  handleData(`http://${lanIP}/api/v1/startup`, showStartupTime);
}
//#endregion

//#region ***  Event Listeners - listenTo___            ***********
const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("connected with socket webserver");
    getStateWindows();
    getTimeWatered();
    getStartupTime();
  });

  socket.on("B2F_latest_data_sensor_soil", function(jsonObject) {
    getSettings();
    const htmlSensorSoil = document.querySelector('.js-sensor-soil');
    htmlSensorSoil.innerHTML = `${jsonObject.sensor.Value} ${jsonObject.sensor.Unit}`;
    let differenceSoil = Math.abs(parseFloat(setSoilMoisture) - parseFloat(jsonObject.sensor.Value));
    if (differenceSoil <= 5) {
      colorIcon('soil','bright-green');
    }
    else if (differenceSoil > 5 & differenceSoil <= 10) {
      colorIcon('soil','light-green');
    }
    else if (differenceSoil > 10 & differenceSoil <= 15) {
      colorIcon('soil','yellow');
    }
    else if (differenceSoil > 15 & differenceSoil <= 20) {
      colorIcon('soil','orange');
    }
    else if (differenceSoil > 20) {
      colorIcon('soil','red');
    }
  });

  socket.on("B2F_latest_data_sensor_eCO2", function(jsonObject) {
    getSettings();
    const htmlSensorCO2 = document.querySelector('.js-sensor-CO2');
    htmlSensorCO2.innerHTML = `${jsonObject.sensor.Value} ${jsonObject.sensor.Unit}`;
    let differenceECO2 = Math.abs(parseFloat(setEco2) - parseFloat(jsonObject.sensor.Value));
    if (differenceECO2 <= 200) {
      colorIcon('co2','bright-green');
    }
    else if (differenceECO2 > 200 & differenceECO2 <= 400) {
      colorIcon('co2','light-green');
    }
    else if (differenceECO2 > 400 & differenceECO2 <= 600) {
      colorIcon('co2','yellow');
    }
    else if (differenceECO2 > 600 & differenceECO2 <= 800) {
      colorIcon('co2','orange');
    }
    else if (differenceECO2 > 800) {
      colorIcon('co2','red');
    }
  });

  socket.on("B2F_latest_data_sensor_temp", function(jsonObject) {
    getSettings();
    const htmlSensorTemp = document.querySelector('.js-sensor-temp');
    htmlSensorTemp.innerHTML = `${jsonObject.sensor.Value} ${jsonObject.sensor.Unit}`;
    let differenceTemp = Math.abs(parseFloat(setTemperature) - parseFloat(jsonObject.sensor.Value));
    if (differenceTemp <= 2) {
      colorIcon('temp','bright-green');
    }
    else if (differenceTemp > 2 & differenceTemp <= 4) {
      colorIcon('temp','light-green');
    }
    else if (differenceTemp > 4 & differenceTemp <= 6) {
      colorIcon('temp','yellow');
    }
    else if (differenceTemp > 6 & differenceTemp <= 8) {
      colorIcon('temp','orange');
    }
    else if (differenceTemp > 8) {
      colorIcon('temp','red');
    }
  });

  socket.on("B2F_latest_data_sensor_humidity", function(jsonObject) {
    getSettings();
    const htmlSensorHumidity = document.querySelector('.js-sensor-humidity');
    htmlSensorHumidity.innerHTML = `${jsonObject.sensor.Value} ${jsonObject.sensor.Unit}`;
    let differenceHumidity = Math.abs(parseFloat(setHumidity) - parseFloat(jsonObject.sensor.Value));
    if (differenceHumidity <= 5) {
      colorIcon('humidity','bright-green');
    }
    else if (differenceHumidity > 5 & differenceHumidity <= 10) {
      colorIcon('humidity','light-green');
    }
    else if (differenceHumidity > 10 & differenceHumidity <= 15) {
      colorIcon('humidity','yellow');
    }
    else if (differenceHumidity > 15 & differenceHumidity <= 20) {
      colorIcon('humidity','orange');
    }
    else if (differenceHumidity > 20) {
      colorIcon('humidity','red');
    }
  });

  socket.on("B2F_latest_data_sensor_light", function(jsonObject) {
    const htmlSensorLight = document.querySelector('.js-sensor-light');
    htmlSensorLight.innerHTML = `${jsonObject.sensor.Value} ${jsonObject.sensor.Unit}`;
    if (jsonObject.sensor.Value >= 40) {
      colorIcon('light','bright-green');
    }
    else if (jsonObject.sensor.Value > 30 & jsonObject.sensor.Value <= 40) {
      colorIcon('light','light-green');
    }
    else if (jsonObject.sensor.Value > 20 & jsonObject.sensor.Value <= 30) {
      colorIcon('light','yellow');
    }
    else if (jsonObject.sensor.Value > 10 & jsonObject.sensor.Value <= 20) {
      colorIcon('light','orange');
    }
    else if (jsonObject.sensor.Value < 10) {
      colorIcon('light','red');
    }
  });

  socket.on("B2F_waterlvl_notification", function(jsonObject) {
    const htmlWaterlvl = document.querySelector('.js-waterlvl');
    let waterlvlString = '';
    if (jsonObject.water_level == 0) {
      waterlvlString = 'NOT OK';
      document.querySelector(`.js-icon-box-water`).classList.remove('c-icon-box--grey');
      document.querySelector('.js-icon-box-water').classList.remove('c-icon-box--blue');
      document.querySelector('.js-icon-box-water').classList.add('c-icon-box--red');
    }
    else {
      waterlvlString = 'OK';
      document.querySelector(`.js-icon-box-water`).classList.remove('c-icon-box--grey');
      document.querySelector('.js-icon-box-water').classList.remove('c-icon-box--red');
      document.querySelector('.js-icon-box-water').classList.add('c-icon-box--blue');
    }
    htmlWaterlvl.innerHTML = `${waterlvlString}`;
  });
  
  socket.on("message", function(data) {
    if (data == 'B2F_change_windows') {
      getStateWindows();
    }
  })
};

const listenToUI = function () {
  document.querySelector('.js-water-btn').addEventListener('click', function() {
    socket.send('F2B_add_water');
    let valueButton = document.querySelector('.js-water-btn').innerHTML 
    if (valueButton == 'Add water') {
      document.querySelector('.js-water-btn').innerHTML = 'Stop adding water';
    }
    else {
      document.querySelector('.js-water-btn').innerHTML = 'Add water';
    }
    getTimeWatered();
  });

  document.querySelector('.js-windows-btn').addEventListener('click', function () {
    socket.send('F2B_change_windows');
    let valueButton2 = document.querySelector('.js-windows-btn').innerHTML;
    if (valueButton2 == 'Open windows') {
      document.querySelector('.js-windows-btn').innerHTML = 'Close windows';
    }
    else {
      document.querySelector('.js-windows-btn').innerHTML = 'Open windows';
    }
    getStateWindows();
  });

  document.querySelector('.js-power-btn').addEventListener('click', function () {
    socket.send('F2B_turn_off');
  });
}

const listenToShowMeasurementsButton = function () {
  document.querySelector('.js-measurements-btn').addEventListener('click', function () {
    let date1 = document.querySelector('.js-select-date1').value;
    let date2 = document.querySelector('.js-select-date2').value;
    let deviceid = document.querySelector('.js-select-data').value;
    handleData(`http://${lanIP}/api/v1/measurements/${deviceid}/${date1}/${date2}`, showMeasurementsDates);
  });
}

const listenToSaveButton = function () {
  document.querySelector('.js-settings-btn').addEventListener('click', function () {
    const json = {temperature: document.querySelector('.js-temp').value, 
    humidity: document.querySelector('.js-humidity').value, 
    soil_moisture: document.querySelector('.js-soil-moisture').value, 
    eco2: document.querySelector('.js-co2').value};
    handleData(`http://${lanIP}/api/v1/settings`, callbackSaveChanges, null, 'PUT', JSON.stringify(json));
    getSettings();
  });
}
//#endregion

//#region ***  Init / DOMContentLoaded                  ***********
document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");
    htmlIndex = document.querySelector('.js-index');
    htmlHistory = document.querySelector('.js-history');
    htmlSettings = document.querySelector('.js-settings');
    if (htmlIndex) {
      getTimeWatered();
      getStateWindows();
      getStartupTime();
      getSettings();
      listenToSocket();
      listenToUI();
    }
    if (htmlHistory) {
      getSensors();
      getDates();
      listenToShowMeasurementsButton();
      //getMeasurementsDates();
    }
    if (htmlSettings) {
      getSettings();
      listenToSaveButton();
    }

    //Mobile navigation
    toggleNav();
});
//#endregion