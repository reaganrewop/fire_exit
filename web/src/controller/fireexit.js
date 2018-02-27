import mongoose from 'mongoose';
import { Router } from 'express';
import Fireexit from '../model/fireexit';
import bodyParser from 'body-parser';

export default({ config, db }) => {
  let api = Router();

  // '/v1/fireexit' - GET all fireexits
  api.get('/', (req, res) => {
    Fireexit.find({}, (err, fireexits) => {
      if (err) {
        res.send(err);
      }
      res.json(fireexits);
    });
  });

  // '/v1/fireexit/:id' - GET a specific fireexit
  api.get('/:id', (req, res) => {
    Fireexit.findById(req.params.id, (err, fireexit) => {
      if (err) {
        res.send(err);
      }
      res.json(fireexit);
    });
  });

  // '/v1/fireexit/add' - POST - add a fireexit
  api.post('/add', (req, res) => {
    let newExit = new Fireexit();
    newExit.blocked = req.body.blocked;

    newExit.save(function(err) {
      if (err) {
        res.send(err);
      }
      res.json({ message: 'Fireexit saved successfully' });
    });
  });

  // '/v1/fireexit/:id' - DELETE - remove a fireexit
  api.delete('/:id', (req, res) => {
    Fireexit.remove({
      _id: req.params.id
    }, (err, fireexit) => {
      if (err) {
        res.send(err);
      }
      res.json({message: "Fireexit Successfully Removed"});
    });
  });

  // '/v1/fireexit/:id' - PUT - update an existing record
  api.put('/:id', (req, res) => {
    Fireexit.findById(req.params.id, (err, fireexit) => {
      if (err) {
        res.send(err);
      }
      fireexit.name = req.body.name;
      fireexit.save(function(err) {
        if (err) {
          res.send(err);
        }
        res.json({ message: 'Fireexit info updated' });
      });
    });
  });

  return api;
}
