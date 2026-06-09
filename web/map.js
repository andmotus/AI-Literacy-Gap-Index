const map = L.map("map", {
  zoomControl: true,
  scrollWheelZoom: true
});

// Storytelling-oriented initial view: mainland Europe.
// Outermost regions remain in the GeoJSON and can be handled separately later.
map.setView([52, 13], 4);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 10,
  attribution: "&copy; OpenStreetMap contributors"
}).addTo(map);

const DATA_PATH = "data/nuts1_ai_literacy_gap.geojson";

const regionInfo = document.getElementById("region-info");

function formatNumber(value, digits = 3) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "No data";
  }
  return Number(value).toFixed(digits);
}

function getColor(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "#d1d5db";
  }

  if (value >= 0.65) return "#800026";
  if (value >= 0.60) return "#bd0026";
  if (value >= 0.55) return "#e31a1c";
  if (value >= 0.50) return "#fc4e2a";
  if (value >= 0.45) return "#fd8d3c";
  if (value >= 0.40) return "#feb24c";
  if (value >= 0.35) return "#fed976";
  return "#ffeda0";
}

function styleRegion(feature) {
  const props = feature.properties;
  const hasData = props.has_index_data === true || props.has_index_data === "True";
  const value = Number(props.ai_literacy_gap_index);

  return {
    fillColor: hasData ? getColor(value) : "#d1d5db",
    weight: 0.8,
    opacity: 1,
    color: "#ffffff",
    fillOpacity: hasData ? 0.85 : 0.75
  };
}

function highlightRegion(event) {
  const layer = event.target;

  layer.setStyle({
    weight: 2.2,
    color: "#111827",
    fillOpacity: 0.95
  });

  layer.bringToFront();
}

function resetHighlight(event) {
  geojsonLayer.resetStyle(event.target);
}

function updateRegionInfo(props) {
  const hasData = props.has_index_data === true || props.has_index_data === "True";

  if (!hasData) {
    regionInfo.innerHTML = `
      <h3 class="region-title">${props.NAME_LATN}</h3>
      <p class="region-meta">${props.CNTR_CODE} · ${props.NUTS_ID}</p>
      <p class="muted">
        No AI Literacy Gap Index value is available for this NUTS-1 region.
      </p>
    `;
    return;
  }

  regionInfo.innerHTML = `
    <h3 class="region-title">${props.nuts1_name || props.NAME_LATN}</h3>
    <p class="region-meta">${props.country || props.CNTR_CODE} · ${props.NUTS_ID}</p>

    <div class="score">${formatNumber(props.ai_literacy_gap_index)}</div>
    <div class="score-label">AI Literacy Gap Index</div>

    <ul class="detail-list">
      <li><span>Rank</span><strong>${props.rank ?? "No data"}</strong></li>
      <li><span>Cluster</span><strong>${props.cluster_label ?? "No data"}</strong></li>
      <li><span>Baseline score</span><strong>${formatNumber(props.baseline_score)}</strong></li>
      <li><span>Pillars available</span><strong>${props.pillars_available ?? "No data"}</strong></li>
      <li><span>P1 Digital skills risk</span><strong>${formatNumber(props.P1_norm)}</strong></li>
      <li><span>P2 Poverty risk</span><strong>${formatNumber(props.P2_norm)}</strong></li>
      <li><span>P3 Low education risk</span><strong>${formatNumber(props.P3_norm)}</strong></li>
      <li><span>P4 Lifelong learning risk</span><strong>${formatNumber(props.P4_norm)}</strong></li>
      <li><span>P5 Low-education unemployment risk</span><strong>${formatNumber(props.P5_norm)}</strong></li>
      <li><span>P6 Ageing risk</span><strong>${formatNumber(props.P6_norm)}</strong></li>
    </ul>
  `;
}

function onEachRegion(feature, layer) {
  const props = feature.properties;

  layer.bindTooltip(
    `${props.NAME_LATN}<br>${formatNumber(props.ai_literacy_gap_index)}`,
    {
      sticky: true,
      direction: "top"
    }
  );

  layer.on({
    mouseover: highlightRegion,
    mouseout: resetHighlight,
    click: function () {
      updateRegionInfo(props);
    }
  });
}

let geojsonLayer;

fetch(DATA_PATH)
  .then(response => {
    if (!response.ok) {
      throw new Error(`Could not load ${DATA_PATH}`);
    }
    return response.json();
  })
  .then(data => {
    geojsonLayer = L.geoJSON(data, {
      style: styleRegion,
      onEachFeature: onEachRegion
    }).addTo(map);

    // Fit initial bounds to mainland-Europe regions only.
    const mainlandLayers = [];

    geojsonLayer.eachLayer(layer => {
      const props = layer.feature.properties;
      const isOutermost =
        props.outside_mainland_europe_extent === true ||
        props.outside_mainland_europe_extent === "True";

      if (!isOutermost) {
        mainlandLayers.push(layer);
      }
    });

    const mainlandGroup = L.featureGroup(mainlandLayers);
    map.fitBounds(mainlandGroup.getBounds(), {
      padding: [20, 20]
    });
  })
  .catch(error => {
    console.error(error);
    regionInfo.innerHTML = `
      <p class="muted">
        The map data could not be loaded. Make sure the page is served through a local web server, not opened directly as a file.
      </p>
    `;
  });

const legend = L.control({ position: "bottomleft" });

legend.onAdd = function () {
  const div = L.DomUtil.create("div", "legend");

  div.innerHTML = `
    <div class="legend-title">Index score</div>
    <div class="legend-row"><span class="legend-color" style="background:#800026"></span> ≥ 0.65</div>
    <div class="legend-row"><span class="legend-color" style="background:#e31a1c"></span> 0.55 – 0.65</div>
    <div class="legend-row"><span class="legend-color" style="background:#fd8d3c"></span> 0.45 – 0.55</div>
    <div class="legend-row"><span class="legend-color" style="background:#fed976"></span> 0.35 – 0.45</div>
    <div class="legend-row"><span class="legend-color" style="background:#ffeda0"></span> < 0.35</div>
    <div class="legend-row"><span class="legend-color" style="background:#d1d5db"></span> No index data</div>
  `;

  return div;
};

legend.addTo(map);
