import { useEffect, useState } from 'react';
import axios from 'axios';
import Graph from './Graph';
import Prediction from './Prediction';
import FiltreMobile from './FiltreMobile';
import WorldMap from './WorldMap';

export default function Dashboard() {
  const [countries, setCountries] = useState([]);
  const [pandemics, setPandemics] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [population, setPopulation] = useState(0);
  const [selectedPandemic, setSelectedPandemic] = useState(null);
  const [statType, setStatType] = useState('daily_new_cases');
  const [stats, setStats] = useState({});
  const [startDate, setStartDate] = useState("2020-01-01");
  const [endDate, setEndDate] = useState("2025-01-01");
  const [transmissionRate, setTransmissionRate] = useState(0);
  const [mortalityRate, setMortalityRate] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      axios.get('http://127.0.0.1:5000/country'),
      axios.get('http://127.0.0.1:5000/pandemic')
    ])
      .then(([res1, res2]) => {
        setCountries(res1.data);
        setPandemics(res2.data);
      })
      .catch(err => console.error("Erreur init:", err))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (selectedCountry) {
      setLoading(true);
      axios.get(`http://127.0.0.1:5000/country/${selectedCountry}`)
        .then(res => {
          if (res.data && res.data.population) {
            setPopulation(res.data.population);
          }
        })
        .catch(err => {
          console.error("Erreur lors de la récupération de la population :", err);
          setPopulation(0);
        })
        .finally(() => setLoading(false));
    }
  }, [selectedCountry]);

  useEffect(() => {
    if (selectedCountry && selectedPandemic) {
      setLoading(true);
      const countryId = Number(selectedCountry);
      const pandemicId = Number(selectedPandemic);
      setTransmissionRate(0);

      const promises = [];

      if (pandemicId === 2) {
        promises.push(
          axios.get(`http://127.0.0.1:5000/daily_pandemic_country/totals/${countryId}/${pandemicId}`)
            .then(res => {
              const { total_cases, total_deaths } = res.data;
              setStats({
                total_confirmed: total_cases,
                total_deaths: total_deaths,
                total_recovered: 0
              });
              const rate = total_cases ? (total_deaths / total_cases) * 100 : 0;
              setMortalityRate(rate.toFixed(2));
            })
            .catch(err => {
              console.error("Erreur récupération totaux Monkeypox:", err);
              setStats({ total_confirmed: 0, total_deaths: 0, total_recovered: 0 });
              setMortalityRate(0);
            })
        );
      } else {
        promises.push(
          axios.get(`http://127.0.0.1:5000/pandemic_country/${selectedCountry}/${selectedPandemic}`)
            .then(res => {
              setStats(res.data);
              const { total_deaths, total_confirmed } = res.data;
              const rate = total_confirmed ? (total_deaths / total_confirmed) * 100 : 0;
              setMortalityRate(rate.toFixed(2));
            })
        );
      }

      promises.push(
        axios.get(`http://127.0.0.1:5000/daily_pandemic_country/${selectedCountry}/${selectedPandemic}`)
          .then(res => {
            const data = res.data.filter(entry => {
              const date = new Date(entry.date);
              return date >= new Date(startDate) && date <= new Date(endDate);
            });

            if (data.length === 0) {
              setTransmissionRate(0);
              return;
            }

            const totalCases = data.reduce((sum, item) => sum + (item.daily_new_cases || 0), 0);
            const meanActive = data.reduce((sum, item) => sum + (item.active_cases || 0), 0) / (data.length || 1);
            const transmission = meanActive ? (totalCases / meanActive) * 100 : 0;
            setTransmissionRate(transmission.toFixed(2));
          })
      );

      Promise.all(promises).finally(() => setLoading(false));
    }
  }, [selectedCountry, selectedPandemic, startDate, endDate]);

  return (
    <div className="p-4 text-black" role="main">
      {loading && (
        <div className="flex justify-center items-center py-6">
          <svg className="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
          </svg>
          <span className="ml-3 text-gray-600 dark:text-gray-300 text-lg font-medium">Chargement des données...</span>
        </div>
      )}

      <FiltreMobile
        countries={countries}
        pandemics={pandemics}
        statType={statType}
        selectedCountry={selectedCountry}
        selectedPandemic={selectedPandemic}
        startDate={startDate}
        endDate={endDate}
        onChangeCountry={e => setSelectedCountry(e.target.value)}
        onChangePandemic={e => setSelectedPandemic(e.target.value)}
        onChangeStatType={e => setStatType(e.target.value)}
        onChangeStartDate={e => setStartDate(e.target.value)}
        onChangeEndDate={e => setEndDate(e.target.value)}
      />

      <div className="flex flex-col md:flex-row gap-6 w-full">
        {/* Filtres à gauche */}
        <div className="hidden md:flex md:w-1/6 flex-col gap-2 shrink-0 sticky top-4 h-fit" role="pays" aria-label="Filtres de sélection">
          <select
            className="p-2 rounded bg-gray-800 text-white text-center"
            onChange={e => setSelectedCountry(e.target.value)}
            defaultValue=""
            aria-label="Sélectionner un pays"
            tabIndex={0}
          >
            <option value="" disabled>Sélectionner un pays</option>
            {countries.map(([id, name]) => (
              <option key={id} value={id}>{name}</option>
            ))}
          </select>

          <select
            className="p-2 rounded bg-gray-800 text-white text-center"
            onChange={e => setSelectedPandemic(e.target.value)}
            defaultValue=""
            aria-label="Sélectionner une pandémie"
            tabIndex={0}
          >
            <option value="" disabled>Sélectionner une pandémie</option>
            {pandemics.map(p => (
              <option key={p.id_pandemic} value={p.id_pandemic}>{p.name}</option>
            ))}
          </select>

          <select
            className="p-2 rounded bg-gray-800 text-white text-center"
            onChange={e => setStatType(e.target.value)}
            value={statType}
            aria-label="Sélectionner un type de statistique"
            tabIndex={0}
          >
            <option value="daily_new_cases">Cas</option>
            <option value="daily_new_deaths">Décès</option>
          </select>

          <input
            type="date"
            value={startDate}
            onChange={e => setStartDate(e.target.value)}
            className="p-2 rounded bg-gray-800 text-white text-center"
            aria-label="Date de début"
            tabIndex={0}
          />
          <input
            type="date"
            value={endDate}
            onChange={e => setEndDate(e.target.value)}
            className="p-2 rounded bg-gray-800 text-white text-center"
            aria-label="Date de fin"
            tabIndex={0}
          />
        </div>

        {/* Contenu principal à droite */}
        <div className="flex-1 flex flex-col gap-6"  aria-label="Statistiques et prévisions">
          {/* Stat Cards */}
          <div className="flex flex-wrap justify-center gap-4"  aria-label="Statistiques clés">
            <div className="w-40 h-28 p-4 bg-primary text-primary-foreground rounded shadow"  aria-label={`Total Confirmed : ${stats.total_confirmed || 0}`} tabIndex={0}>
              <h3 className="text-lg font-semibold">Total Confirmed</h3>
              <p className="text-2xl font-bold">{stats.total_confirmed || 0}</p>
            </div>
            <div className="w-40 h-28 p-4 bg-destructive text-destructive-foreground rounded shadow"  aria-label={`Total Deaths : ${stats.total_deaths || 0}`} tabIndex={0}>
              <h3 className="text-lg font-semibold">Total Deaths</h3>
              <p className="text-2xl font-bold">{stats.total_deaths || 0}</p>
            </div>
            <div className="w-40 h-28 p-4 bg-accent text-accent-foreground rounded shadow"  aria-label={`Total Recovered : ${stats.total_recovered || 0}`} tabIndex={0}>
              <h3 className="text-lg font-semibold">Total Recovered</h3>
              <p className="text-2xl font-bold">{stats.total_recovered || 0}</p>
            </div>
            <div className="w-40 h-28 p-4 bg-muted text-muted-foreground rounded shadow"  aria-label={`Mortality Rate : ${mortalityRate}%`} tabIndex={0}>
              <h3 className="text-lg font-semibold">Mortality Rate</h3>
              <p className="text-2xl font-bold">{mortalityRate}%</p>
            </div>
            <div className="w-40 h-28 p-4 bg-muted text-muted-foreground rounded shadow"  aria-label={`Transmission Rate : ${transmissionRate}%`} tabIndex={0}>
              <h3 className="text-lg font-semibold">Transmission Rate</h3>
              <p className="text-2xl font-bold">{transmissionRate}%</p>
            </div>
            <div className="w-40 h-28 p-4 bg-secondary text-secondary-foreground rounded shadow" aria-label={`Population : ${population}`} tabIndex={0}>
              <h3 className="text-lg font-semibold">Population</h3>
              <p className="text-2xl font-bold">{population}</p>
            </div>
          </div>

          {/* Graphes */}
          <Graph
            countryId={selectedCountry}
            pandemicId={selectedPandemic}
            statType={statType}
            startDate={startDate}
            endDate={endDate}
          />
          <Prediction
            statType={statType}
            countryId={selectedCountry}
            pandemicId={selectedPandemic}
          />
          <WorldMap pandemicId={selectedPandemic} />
        </div>
      </div>
    </div>
  );
}
