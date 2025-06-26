import React, { useEffect, useState } from "react";
import { Line, Pie, Bar } from "react-chartjs-2";
import axios from "axios";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
} from "chart.js";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement
);

const Graph = ({ countryId, pandemicId, startDate, endDate, statType }) => {
  const [lineData, setLineData] = useState(null);
  const [pieData, setPieData] = useState(null);
  const [barData, setBarData] = useState(null);

  useEffect(() => {
    if (!countryId || !pandemicId || !statType || !startDate || !endDate) return;

    axios
      .get(`http://localhost:5000/daily_pandemic_country/${countryId}/${pandemicId}`)
      .then((res) => {
        const data = res.data;
        const filtered = data.filter((item) => {
          const date = new Date(item.date);
          return date >= new Date(startDate) && date <= new Date(endDate);
        });

        if (filtered.length > 0) {
          setLineData({
            labels: filtered.map((d) => new Date(d.date).toISOString().split("T")[0]),
            datasets: [
              {
                label: statType.replace("_", " "),
                data: filtered.map((d) => Number(d[statType]) || 0),
                borderColor: "rgba(255, 99, 132, 1)",
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                tension: 0.4,
                fill: true,
              },
            ],
          });
        } else {
          setLineData(null);
        }
      })
      .catch((err) => {
        console.error("Erreur ligne :", err);
        setLineData(null);
      });
  }, [countryId, pandemicId, startDate, endDate, statType]);

 useEffect(() => {
  const url =
    pandemicId === "1" || pandemicId === 1
      ? "http://localhost:5000/pandemic_country/continent"
      : "http://localhost:5000/daily_pandemic_country/monkeypox/continent";

  axios
    .get(url)
    .then((res) => {
      const data = res.data;
      const labels = data.map((d) => d.continent);
      const values = data.map((d) =>
        statType === "daily_new_deaths" ? d.total_deaths : d.total_confirmed
      );

      setPieData({
        labels,
        datasets: [
          {
            label: "Répartition par continent",
            data: values,
            backgroundColor: [
              "#FF6384",
              "#36A2EB",
              "#FFCE56",
              "#4BC0C0",
              "#9966FF",
              "#F7464A",
            ],
          },
        ],
      });
    })
    .catch((err) => {
      console.error("Erreur camembert :", err);
      setPieData(null);
    });
}, [statType, pandemicId]);


  useEffect(() => {
    axios
      .get("http://localhost:5000/predictions/active_cases")
      .then((res) => {
        const data = res.data;

        const labels = data.map((d) => d.country);
        const values = data.map((d) => Math.round(d.predicted_active_cases));

        setBarData({
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
      .catch((err) => {
        console.error("Erreur barres :", err);
        setBarData(null);
      });
  }, []);

  return (
    <div className="flex flex-col md:flex-row justify-center gap-10 mt-10">
      {/* Line Chart */}
      <div
        className="w-full md:w-1/2 bg-white p-4 rounded shadow"
        style={{ height: "350px" }}
        role="region"
        aria-label="Graphique en courbes des données temporelles"
        tabIndex={0}
      >
        {lineData ? (
          <Line
            data={lineData}
            options={{
              responsive: true,
              maintainAspectRatio: false,
            }}
          />
        ) : (
          <p>Aucune donnée disponible pour ce pays sur cette période.</p>
        )}
      </div>

      {/* Pie Chart */}
      <div
        className="w-full md:w-1/2 bg-white p-4 rounded shadow"
        style={{ height: "350px" }}
        role="region"
        aria-label="Diagramme circulaire des cas par continent"
        tabIndex={0}
      >
        {pieData ? (
          <Pie
            data={pieData}
            options={{
              responsive: true,
              maintainAspectRatio: false,
            }}
          />
        ) : (
          <p>Données continentales indisponibles pour cette pandémie.</p>
        )}
      </div>
    </div>
  );
};

export default Graph;
