import { MapContainer, TileLayer, Circle, Tooltip } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { useEffect, useState } from 'react';
import axios from 'axios';
import countryCoordinates from './countrycoords';

export default function WorldMap({ pandemicId }) {
  const [countries, setCountries] = useState([]);

  useEffect(() => {
    if (pandemicId) {
      axios
        .get(`http://127.0.0.1:5000/predict/next_wave_risk/${pandemicId}`)
        .then(res => setCountries(res.data))
        .catch(err => console.error('Erreur lors de la récupération des données :', err));
    }
  }, [pandemicId]);

  const getColor = (risk) => {
    if (risk === 'faible') return 'green';
    if (risk === 'modéré') return 'orange';
    return 'red';
  };

  const getRadius = (risk) => {
    if (risk === 'élevé') return 200000;
    if (risk === 'modéré') return 100000;
    if (risk === 'faible') return 80000;
    return 20000;
  };

  return (
    <div className="h-[500px] w-full">
      <MapContainer
        center={[20, 0]}
        zoom={2}
        minZoom={2}
        maxZoom={6}
        style={{ height: '100%', width: '100%' }}
        worldCopyJump={false}
        maxBounds={[[-85, -180], [85, 180]]}
        maxBoundsViscosity={1.0}
        zoomControl={false}
      >
      <TileLayer
      url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
      attribution='&copy; <a href="https://carto.com/">CARTO</a>'
    />

        {countries.map((country, index) => {
          const coords = countryCoordinates[country.country_name];
          if (!coords) return null;

          return (
            <Circle
              key={index}
              center={coords}
              radius={getRadius(country.risk_level)}
              pathOptions={{ color: getColor(country.risk_level), fillOpacity: 0.5 }}
            >
              <Tooltip direction="top" offset={[0, -10]} opacity={1}>
                <div className="text-sm">
                  <strong>{country.country_name}</strong><br />
                  Risque : {country.risk_level}
                </div>
              </Tooltip>
            </Circle>
          );
        })}
      </MapContainer>
    </div>
  );
}
