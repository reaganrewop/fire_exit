import mongoose from 'mongoose';
const Schema = mongoose.Schema;

let Account = new Schema({
  email: String,
  password: String
});

module.exports = mongoose.model('Account', Account);
