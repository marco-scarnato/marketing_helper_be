const creativehubDb = db.getSiblingDB('creativehub');

creativehubDb.getCollection('_init').insertOne({
  initialized: true,
  at: new Date()
});
