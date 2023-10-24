/* const flix = require('flix');
flix.stations.all({ apiKey: '42b9ce3e3cmsh04d07062ba49f04p153e5ajsn738cd8121ff3' }).on('data', item => {
  console.log(item)
}); */

const axios = require('axios');

const options = {
  method: 'GET',
  url: 'https://flixbus2.p.rapidapi.com/trips',
  params: {
    from_id: '40de8044-8646-11e6-9066-549f350fcb0c',
    to_id: '40dea87d-8646-11e6-9066-549f350fcb0c',
    date: '16.12.2023',
    adult: '1',
    children: '0',
    bikes: '0',
    currency: 'EUR'
  },
  headers: {
    'X-RapidAPI-Key': '42b9ce3e3cmsh04d07062ba49f04p153e5ajsn738cd8121ff3',
    'X-RapidAPI-Host': 'flixbus2.p.rapidapi.com'
  }
};

async function test () {
  try {
    const response = await axios.request(options);
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
}
test();

/*
const axios = require('axios');

const options = {
  method: 'GET',
  url: 'https://flixbus2.p.rapidapi.com/schedule',
  params: {
    station_id: 'dcbd21fc-9603-11e6-9066-549f350fcb0c',
    date: '15.05.2022'
  },
  headers: {
    'X-RapidAPI-Key': '42b9ce3e3cmsh04d07062ba49f04p153e5ajsn738cd8121ff3',
    'X-RapidAPI-Host': 'flixbus2.p.rapidapi.com'
  }
};

try {
	const response = await axios.request(options);
	console.log(response.data);
} catch (error) {
	console.error(error);
}
*/