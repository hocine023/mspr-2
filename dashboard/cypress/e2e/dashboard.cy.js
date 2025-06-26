describe('Dashboard E2E', () => {
  beforeEach(() => {
    cy.intercept('GET', '**/country').as('getCountries');
    cy.intercept('GET', '**/country/*').as('getCountryById');
    cy.intercept('GET', '**/pandemic').as('getPandemics');
    cy.intercept('GET', '**/pandemic_country/continent').as('getPie');
    cy.intercept('GET', '**/pandemic_country/*/*').as('getCountryStatsClassic');
    cy.intercept('GET', '**/daily_pandemic_country/totals/*/*').as('getCountryStatsMonkeypox');
    cy.intercept('GET', '**/daily_pandemic_country/**').as('getDailyStats');
    cy.intercept('GET', '**/predict/**').as('getPredictions');
  });

  const testConfig = [
    { country: 'France', pandemic: 'COVID-19', stat: 'Cas' },
    { country: 'France', pandemic: 'MPOX', stat: 'Décès' },
    { country: 'Brazil', pandemic: 'COVID-19', stat: 'Cas' },
    { country: 'Brazil', pandemic: 'MPOX', stat: 'Décès' },
  ];

  testConfig.forEach(({ country, pandemic, stat }) => {
    it(`affiche les graphiques pour ${country} - ${pandemic} - ${stat}`, () => {
      cy.visit('http://localhost:5173');

      cy.wait('@getCountries', { timeout: 10000 });
      cy.wait('@getPandemics', { timeout: 10000 });
      cy.wait(1000);

      // Sélection pays
      cy.get('select[aria-label="Sélectionner un pays"]')
        .should('be.visible')
        .select(country);
      cy.wait('@getCountryById', { timeout: 10000 });
      cy.wait(1000);

      // Sélection pandémie
      cy.get('select[aria-label="Sélectionner une pandémie"]')
        .should('be.visible')
        .find('option')
        .should('contain.text', pandemic);
      cy.get('select[aria-label="Sélectionner une pandémie"]').select(pandemic);

      if (pandemic === 'MPOX') {
        cy.wait('@getCountryStatsMonkeypox', { timeout: 10000 });
      } else {
        cy.wait('@getCountryStatsClassic', { timeout: 10000 });
      }

      cy.wait(1000);

      // Sélection type de statistique
      cy.get('select[aria-label="Sélectionner un type de statistique"]')
        .should('be.visible')
        .select(stat);
      cy.wait(1000);

      const startDate = pandemic === 'MPOX' ? '2023-05-01' : '2021-05-01';
      const endDate = pandemic === 'MPOX' ? '2023-05-10' : '2021-05-10';

      cy.get('input[type="date"]').eq(0).clear().type(startDate);
      cy.get('input[type="date"]').eq(1).clear().type(endDate);
      cy.wait(1000);

      // Vérifications : Graphiques présents
      cy.wait('@getDailyStats', { timeout: 20000 });
      cy.wait('@getPredictions', { timeout: 20000 });

      cy.get('[aria-label="Graphique en courbes des données temporelles"]', { timeout: 10000 })
        .should('exist');

      // Histogrammes de prédiction
      cy.get('[aria-label="Histogramme des cas actifs prédits par pays"]', { timeout: 15000 })
        .should('be.visible');

      const predictedLabel = stat === 'Décès'
        ? 'Histogramme des décès prédits'
        : 'Histogramme des cas prédits';

      cy.get(`[aria-label="${predictedLabel}"]`, { timeout: 15000 })
        .should('be.visible');
      cy.wait(10000);
    });
  });
});
