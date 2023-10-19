const flix = require('flix');
flix.stations.all().on('data', item => {
  console.log(item)
});
