import express from 'express';
import config from '../config';
import initializeDb from '../db';
import middleware from '../middleware';
import fireexit from '../controller/fireexit';

let router = express();

// connect to db
initializeDb(db => {

  // internal middleware
  router.use(middleware({ config, db }));

  // api routes v1 (/v1)
  router.use('/fireexit', fireexit({ config, db }));
});

export default router;
