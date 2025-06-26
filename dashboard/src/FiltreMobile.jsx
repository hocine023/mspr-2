import React, { useState } from 'react';

export default function FiltreMobile({
  countries,
  pandemics,
  statType,
  selectedCountry,
  selectedPandemic,
  startDate,
  endDate,
  onChangeCountry,
  onChangePandemic,
  onChangeStatType,
  onChangeStartDate,
  onChangeEndDate
}) {
  const [open, setOpen] = useState(false);

  return (
    <div className="md:hidden mb-4">
      <button
        onClick={() => setOpen(!open)}
        className="bg-gray-800 text-white px-4 py-2 rounded"
      >
        {open ? 'Fermer les filtres' : 'ouvrir les filtres'}
      </button>

      {open && (
        <div className="mt-4 flex flex-col gap-2">
          <select className="p-2 rounded bg-gray-800 text-white" value={selectedCountry} onChange={onChangeCountry}>
            <option value="" disabled>Sélectionner un pays</option>
            {countries.map(([id, name]) => (
              <option key={id} value={id}>{name}</option>
            ))}
          </select>

          <select className="p-2 rounded bg-gray-800 text-white" value={selectedPandemic} onChange={onChangePandemic}>
            <option value="" disabled>Sélectionner une pandémie</option>
            {pandemics.map(p => (
              <option key={p.id_pandemic} value={p.id_pandemic}>{p.name}</option>
            ))}
          </select>

          <select className="p-2 rounded bg-gray-800 text-white" value={statType} onChange={onChangeStatType}>
            <option value="daily_new_cases">Cas</option>
            <option value="daily_new_deaths">Décès</option>
          </select>

          <input type="date" className="p-2 rounded bg-gray-800 text-white" value={startDate} onChange={onChangeStartDate} />
          <input type="date" className="p-2 rounded bg-gray-800 text-white" value={endDate} onChange={onChangeEndDate} />
        </div>
      )}
    </div>
  );
}
