import mongoose from 'mongoose';
let Schema = mongoose.Schema;

let fireexitSchema = new Schema({
  blocked: String
});

module.exports = mongoose.model('Fireexit', fireexitSchema);
