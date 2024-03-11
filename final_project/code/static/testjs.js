function sendData() {
    var address = document.getElementById('address').value;
    var berth = document.getElementById('berth').value;
    var land_area = document.getElementById('land_area').value;
    var tot_floor = document.getElementById('tot_floor').value;
    var room_age = document.getElementById('room_age').value;
    var build_area = document.getElementById('build_area').value;
    var room = document.getElementById('room').value;
    var data = {
      'address': address,
      'berth': berth,
      'land_area': land_area,
      'tot_floor': tot_floor,
      'room_age': room_age,
      'build_area': build_area,
      'room': room
    };
  
    fetch('/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
      // 在這裡處理後端返回的結果
      var resultField = document.getElementById('result');
      resultField.value = '預測結果：' + result.prediction + '/ 坪';
      nearestStationResult.textContent = '最近火車站名稱: ' + result.nearest_trastation_name;
      nearestMRTStationResult.textContent = '最近捷運站名稱: ' + result.nearest_metrostation_name;
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
  