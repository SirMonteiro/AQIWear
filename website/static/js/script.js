document.addEventListener("DOMContentLoaded", () => {
  (document.querySelectorAll(".notification .delete") || []).forEach(
    ($delete) => {
      const $notification = $delete.parentNode;

      $delete.addEventListener("click", () => {
        $notification.parentNode.removeChild($notification);
      });
    },
  );
});

const webBluetoothNotification = document.getElementById(
  "browser-notification",
);

if (!navigator.bluetooth) {
  webBluetoothNotification.style.display = "block";
}

const mapContainer = document.getElementById("map-container");
const mapBtn = document.getElementById("map-btn");
const mapCloseBtn = document.getElementById("map-close-btn");
const mapDiv = document.getElementById("map");
const footerElement = document.getElementsByTagName("footer")[0];

// Initialize OpenStreetMap
const map = L.map("map").setView([-23.482094, -46.499804], 13); // Default coordinates
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// Get current location
navigator.geolocation.getCurrentPosition((position) => {
  const { latitude, longitude } = position.coords;
  map.setView([latitude, longitude], 15);
});

// Add search control
const provider = new GeoSearch.OpenStreetMapProvider();
const searchControl = new GeoSearch.GeoSearchControl({
  provider: provider,
  style: "bar",
  autoComplete: true,
  autoCompleteDelay: 250,
  showMarker: true,
});

map.addControl(searchControl);

const locateControl = L.control({ position: "topleft" });
locateControl.onAdd = function () {
  const div = L.DomUtil.create("div", "leaflet-bar leaflet-control");
  div.innerHTML =
    '<button id="locate-btn" title="Go to Current Location" style="padding: 8px; background: white; border: none;"><i class="bx bx-target-lock"></i></button>';
  return div;
};
locateControl.addTo(map);

document.getElementById("locate-btn").addEventListener("click", () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        map.setView([latitude, longitude], 15);
        L.marker([latitude, longitude])
          .addTo(map)
          .bindPopup("Você está aqui!")
          .openPopup();
      },
      () => {
        alert("Unable to retrieve your location.");
      },
    );
  } else {
    alert("Geolocation is not supported by your browser.");
  }
});

mapBtn.addEventListener("click", () => {
  mapBtn.style.display = "none";
  mapCloseBtn.style.display = "flex";
  mapDiv.style.height = "100vh";
  map.invalidateSize(true);
  footerElement.style.display = "none";
  document.body.style.overflow = "hidden";
});

mapCloseBtn.addEventListener("click", () => {
  mapBtn.style.display = "flex";
  mapCloseBtn.style.display = "none";
  mapDiv.style.height = "0";
  footerElement.style.display = "block";
  document.body.style.overflow = "visible";
});

const temperature = document.getElementById("temperature");
// const humidity = document.getElementById("humidity");
// const dewPoint = document.getElementById("dew-point");
const CO2 = document.getElementById("CO2");
const VOC = document.getElementById("VOC");
const PPM25 = document.getElementById("PPM25");
const PPM1 = document.getElementById("PPM1");

const bluetoothBtn = document.getElementById("bluetooth-btn");
const bluetoothNotification = document.getElementById("bluetooth-notification");

const serviceUUID = "0000181a-0000-1000-8000-00805f9b34fb";

const characteristics = {
  temperature: "00002a6e-0000-1000-8000-00805f9b34fb",
  humidity: "00002a6f-0000-1000-8000-00805f9b34fb",
  dewPoint: "00002a7b-0000-1000-8000-00805f9b34fb",
  CO2: "00002b8c-0000-1000-8000-00805f9b34fb",
  VOC: "00002be7-0000-1000-8000-00805f9b34fb",
  PPM25: "00002bd6-0000-1000-8000-00805f9b34fb",
  PPM1: "00002bd5-0000-1000-8000-00805f9b34fb",
};

let device;
let server;

async function handleCharacteristic(
  service,
  characteristicUUID,
  element,
  divideper100 = true,
) {
  try {
    const characteristic = await service.getCharacteristic(characteristicUUID);
    await characteristic.startNotifications();
    characteristic.addEventListener("characteristicvaluechanged", (event) => {
      const value = event.target.value;
      const dataView = new DataView(value.buffer);
      const decodedValue = dataView.getInt16(0, true); // Little-endian
      if (divideper100) {
        textValue = decodedValue / 100;
      } else {
        textValue = decodedValue;
      }
      element.textContent = textValue;
      changeColor(element, textValue);
    });
  } catch (error) {
    console.error(
      `Error processing characteristic ${characteristicUUID}:`,
      error,
    );
  }
}

bluetoothBtn.addEventListener("click", async () => {
  try {
    device = await navigator.bluetooth.requestDevice({
      filters: [{ services: [serviceUUID] }],
      optionalServices: [serviceUUID],
    });

    server = await device.gatt.connect();
    if (server.connected) {
      bluetoothBtn.style.display = "none";
      bluetoothNotification.parentNode.removeChild(bluetoothNotification);
    }
    const service = await server.getPrimaryService(serviceUUID);

    // Handle all characteristics
    await handleCharacteristic(
      service,
      characteristics.temperature,
      temperature,
    );
    // await handleCharacteristic(service, characteristics.humidity, humidity);
    // await handleCharacteristic(service, characteristics.dewPoint, dewPoint);
    await handleCharacteristic(
      service,
      characteristics.CO2,
      CO2,
      (divideper100 = false),
    );
    await handleCharacteristic(
      service,
      characteristics.VOC,
      VOC,
      (divideper100 = false),
    );
    await handleCharacteristic(service, characteristics.PPM25, PPM25);
    await handleCharacteristic(service, characteristics.PPM1, PPM1);
  } catch (error) {
    console.error("Bluetooth connection failed:", error);
  }
});

function changeColor(element, value) {
  tag = element.parentNode;
  // console.log(element.id);
  switch (element.id) {
    case "temperature":
      limit = 36;
      break;
    case "CO2":
      limit = 1000;
      break;
    case "VOC":
      limit = 100;
      break;
    case "PPM1":
      limit = 4.8;
      break;
    case "PPM25":
      limit = 12;
      break;
  }
  if (value > limit) {
    // console.log(value);
    tag.classList.remove("is-primary");
    tag.classList.add("is-warning");
  } else {
    tag.classList.remove("is-warning");
    tag.classList.add("is-primary");
  }
  updateAQIStatus();
}

function updateAQIStatus() {
  const sensors = document.querySelectorAll(".sensor-tag");
  let isWarning = false;

  // Check if any sensor has a warning status
  sensors.forEach((sensor) => {
    if (sensor.classList.contains("is-warning")) {
      isWarning = true;
    }
  });

  // Update AQI status based on the result
  const AQI = document.getElementById("AQI");
  if (isWarning) {
    AQI.innerText = "Moderado";
    AQI.parentNode.classList.remove("is-primary");
    AQI.parentNode.classList.add("is-warning");
  } else {
    AQI.innerText = "BOM";
    AQI.parentNode.classList.remove("is-warning");
    AQI.parentNode.classList.add("is-primary");
  }
}

mapBtn.addEventListener("click", () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        map.setView([latitude, longitude], 15);

        // Create or update the circle with real-time data
        const circle = L.circle([latitude, longitude], {
          color: "cyan", // Color of the circle border
          fillColor: "cyan", // Fill color of the circle
          fillOpacity: 0.5, // Opacity of the fill
          radius: 100, // Initial radius in meters (update dynamically if needed)
        }).addTo(map);

        // Update the circle's popup with current data
        const popupContent = `
          <strong>Data at Current Location:</strong><br>
          Temperature: ${temperature.textContent}°C<br>
          CO2: ${CO2.textContent} ppm<br>
          VOC: ${VOC.textContent} ppb<br>
          PPM 2.5: ${PPM25.textContent} ppm<br>
          PPM 1: ${PPM1.textContent} ppm
        `;
        circle.bindPopup(popupContent).openPopup();
      },
      () => {
        alert("Unable to retrieve your location.");
      },
    );
  } else {
    alert("Geolocation is not supported by your browser.");
  }
});
