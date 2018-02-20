import mongoose from 'mongoose';
import { Router } from 'express';
import Restaurant from '../model/restaurant';
import bodyParser from 'body-parser';

export default({ config, db }) => {
  let api = Router();

  // '/v1/restaurant' - GET all restaurants
  api.get('/', (req, res) => {
    Restaurant.find({}, (err, restaurants) => {
      if (err) {
        res.send(err);
      }
      res.json(restaurants);
    });
  });

  // '/v1/restaurant/:id' - GET a specific restaurant
  api.get('/:id', (req, res) => {
    Restaurant.findById(req.params.id, (err, restaurant) => {
      if (err) {
        res.send(err);
      }
      res.json(restaurant);
    });
  });

  // '/v1/restaurant/add' - POST - add a restaurant
  api.post('/add', (req, res) => {
    let newRest = new Restaurant();
    newRest.name = req.body.name;

    newRest.save(function(err) {
      if (err) {
        res.send(err);
      }
      res.json({ message: 'Restaurant saved successfully' });
    });
  });

  // '/v1/restaurant/:id' - DELETE - remove a restaurant
  api.delete('/:id', (req, res) => {
    Restaurant.remove({
      _id: req.params.id
    }, (err, restaurant) => {
      if (err) {
        res.send(err);
      }
      res.json({message: "Restaurant Successfully Removed"});
    });
  });

  // '/v1/restaurant/:id' - PUT - update an existing record
  api.put('/:id', (req, res) => {
    Restaurant.findById(req.params.id, (err, restaurant) => {
      if (err) {
        res.send(err);
      }
      restaurant.name = req.body.name;
      restaurant.save(function(err) {
        if (err) {
          res.send(err);
        }
        res.json({ message: 'Restaurant info updated' });
      });
    });
  });

  return api;
}
