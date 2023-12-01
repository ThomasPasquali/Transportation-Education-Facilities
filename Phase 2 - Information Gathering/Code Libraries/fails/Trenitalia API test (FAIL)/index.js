/* const Trenapi = require('./trenapi');
const fs = require('fs');

const trenapi = new Trenapi();
const date = '23/10/2023';
const ROMA = "Roma Termini";
const MILANO = "Milano Centrale";

async function test () {
  let result = await trenapi.getOneWaySolutions(ROMA, MILANO, date, 15, 2, 0, false, false);
  const tratta = result[0];
  const idSoluzione = tratta.idsolution;
  console.log(result);
  fs.writeFileSync('./test.html', result);
  result = await trenapi.getSolutionDetails(idSoluzione);
  // console.log(result);
  result = await trenapi.getSolutionInfo(idSoluzione);
  // console.log(result);

  result = await trenapi.getPriceDetails(idSoluzione);
  // console.log(result);

  result = await trenapi.getCustomizedPriceDetails(idSoluzione);
  //console.log(result);
}
test(); */

const Trenitalia = require('./trenapi');
const moment = require('moment');
(async () => {
    const t = new Trenitalia();
 
    const stations_from = await t.autocomplete("milano");
    const station_from = stations_from[0].name;
    const stations_to = await t.autocomplete("bari");
    const station_to = stations_to[0].name;
    console.log(`Partenza da: ${station_from}, arrivo a: ${station_to}`);
 
    const date = moment().add(3, 'months').format("DD/MM/YYYY");
    const solutions = await t.getOneWaySolutions(station_from, station_to, date, "13", 2, 0);
    console.log(solutions);
    const firstSolution = solutions[0];
    console.log('=== Prima soluzione disponibile ===');
    console.log(`Treno da:\t${firstSolution.origin}`);
    console.log(`Treno a:\t${firstSolution.destination}`);
    console.log(`Partenza:\t${new Date(firstSolution.departuretime)}`);
    console.log(`Arrivo: \t${new Date(firstSolution.arrivaltime)}`);
    console.log(`Prezzo minimo:\t${firstSolution.minprice}`);
    console.log(`Durata: \t${firstSolution.duration}`);
    console.log(`Numero cambi:\t${firstSolution.changesno}`);
    console.log(`Treni:  \t${firstSolution.trainlist.map(x => x.trainidentifier).join(', ')}`);
 
    const priceDetail = await t.getCustomizedPriceDetails(firstSolution.idsolution);
    console.log('=== Alcune possibilità dalla prima soluzione ===');
    let result = '';
    for (const service of priceDetail.leglist[0].travelerlist[0].servicelist) {
        const firstOffer = service.offerlist[0];
        result += `${service.name.padEnd(25)}\t${firstOffer.name.padEnd(15)}\t${firstOffer.points || 0} punti \t${firstOffer.price || 0}€\t${firstOffer.available || 0} posti disponibili ${firstOffer.visible ? '' : '(non visibile)'}\n`
        const secondOffer = service.offerlist[1];
        result += `${'-'.padEnd(25)}\t${secondOffer.name.padEnd(15)}\t${secondOffer.points || 0} punti \t€${secondOffer.price || 0}\t${secondOffer.available || 0} posti disponibili ${secondOffer.visible ? '' : '(non visibile)'}\n`
    };
    console.log(result);
})();