import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const Prediction = ({ countryId, pandemicId, statType }) => {
  const [barData, setBarData] = useState(null);
  const [activeCasesData, setActiveCasesData] = useState(null);

  useEffect(() => {
    if (!countryId || !pandemicId || !statType) return;

    const statPath = statType === 'daily_new_deaths' ? 'deaths' : 'cases';

    axios.get(`http://localhost:5000/predict/${statPath}/${countryId}/${pandemicId}`)
      .then(res => {
        const data = res.data;

        const values = data.map(p =>
          statType === 'daily_new_deaths' ? p.predicted_deaths : p.predicted_cases
        );
        const maxValue = Math.max(...values);

        const backgroundColors = values.map(val => {
          const intensity = val / maxValue;
          const red = 255;
          const green = Math.round(255 * (1 - intensity));
          const blue = Math.round(255 * (1 - intensity));
          return `rgb(${red}, ${green}, ${blue})`;
        });

        setBarData({
          labels: data.map(p => p.date),
          datasets: [{
            label: statType === 'daily_new_deaths' ? 'Décès prédits' : 'Cas prédits',
            data: values,
            backgroundColor: backgroundColors,
          }]
        });
      })
      .catch(err => {
        console.error("Erreur prédiction :", err);
        setBarData(null);
      });
  }, [countryId, pandemicId, statType]);

useEffect(() => {
  if (!countryId || !pandemicId) return;

  axios.get(`http://localhost:5000/predict/active_cases/${countryId}/${pandemicId}`)
    .then(res => {
      const data = res.data;

      if (!Array.isArray(data) || data.length === 0) {
        console.warn("Données vides pour les cas actifs prédits.");
        setActiveCasesData(null);
        return;
      }

      const labels = data.map((d) => d.date);
      const values = data.map((d) => {
        const value = d.predicted_active_cases;
        return typeof value === 'number' ? Math.round(value) : 0;
      });


      setActiveCasesData({
        labels,
        datasets: [
          {
            label: "Prédictions des cas actifs",
            data: values,
            backgroundColor: "rgba(54, 162, 235, 0.5)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
          },
        ],
      });
    })
    .catch(err => {
      console.error("Erreur lors de la récupération des cas actifs prédits :", err);
      setActiveCasesData(null);
    });
}, [countryId, pandemicId]);


  const ariaDescription = statType === 'daily_new_deaths'
    ? 'Histogramme des décès prédits'
    : 'Histogramme des cas prédits';

  return (
    <div className="flex flex-col md:flex-row justify-center gap-6 mt-10">
      {/* Cas actifs par pays */}
      <div
        className="w-full md:w-1/2 bg-white p-4 rounded shadow"
        style={{ height: '350px' }}
        role="region"
        aria-label="Histogramme des cas actifs prédits par pays"
        tabIndex={0}
      >
        {activeCasesData ? (
          <Bar
            data={activeCasesData}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                y: {
                  beginAtZero: true,
                  ticks: {
                    precision: 0,
                  },
                },
              },
            }}
          />
        ) : (
          <p>Aucune donnée de cas actifs prédits disponible pour ce pays.</p>
        )}
      </div>

      {/* Cas/décès prédits dans le temps */}
      <div
        className="w-full md:w-1/2 bg-white p-4 rounded shadow"
        style={{ height: '350px' }}
        role="region"
        aria-label={ariaDescription}
        tabIndex={0}
      >
        {barData ? (
          <Bar
            data={barData}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                y: {
                  beginAtZero: true,
                  ticks: {
                    precision: 0,
                  },
                },
              },
            }}
          />
        ) : (
          <p>{ariaDescription} Impossible de prédire {statType === 'daily_new_deaths' ? 'les décès' : 'les cas'} pour ce pays</p>
        )}
      </div>
    </div>
  );
};

export default Prediction;
