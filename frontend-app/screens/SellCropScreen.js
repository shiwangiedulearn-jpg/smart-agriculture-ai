import React, { useState } from 'react';
import { View, Text, StyleSheet, Alert, ScrollView } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import Button from '../components/Button';
import Input from '../components/Input';
import Card from '../components/Card';
import { sellCrop } from '../services/api';

const SellCropScreen = () => {
  const [cropName, setCropName] = useState('');
  const [quantity, setQuantity] = useState('');
  const [price, setPrice] = useState('');
  const [location, setLocation] = useState('');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const navigation = useNavigation();

  const handleSubmit = async () => {
    if (!cropName || !quantity || !price || !location) {
      Alert.alert('Error', 'Please fill in all required fields');
      return;
    }

    const cropData = {
      seller_user_id: 'demo_user', // This would come from auth context
      crop_name: cropName,
      quantity_kg: parseFloat(quantity),
      price_per_kg: parseFloat(price),
      location: location,
      notes: notes || '',
    };

    setLoading(true);
    try {
      const response = await sellCrop(cropData);
      Alert.alert('Success', 'Your crop has been listed successfully!');
      navigation.navigate('Home');
    } catch (error) {
      Alert.alert('Error', error.detail || 'Failed to list crop');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Card title="List Your Crop for Sale">
        <Input
          label="Crop Name *"
          value={cropName}
          onChangeText={setCropName}
          placeholder="e.g., Tomatoes, Potatoes, Wheat"
        />
        
        <Input
          label="Quantity (kg) *"
          value={quantity}
          onChangeText={setQuantity}
          placeholder="Enter quantity in kilograms"
          keyboardType="numeric"
        />
        
        <Input
          label="Price per kg *"
          value={price}
          onChangeText={setPrice}
          placeholder="Enter price per kilogram"
          keyboardType="numeric"
        />
        
        <Input
          label="Location *"
          value={location}
          onChangeText={setLocation}
          placeholder="e.g., Bengaluru, Mumbai, Delhi"
        />
        
        <Input
          label="Additional Notes"
          value={notes}
          onChangeText={setNotes}
          placeholder="Quality, variety, organic certification, etc."
          multiline
        />
      </Card>

      <Card title="Market Tips">
        <Text style={styles.tipText}>💡 Set competitive prices based on current market rates</Text>
        <Text style={styles.tipText}>🌾 Mention crop quality and variety for better visibility</Text>
        <Text style={styles.tipText}>📍 Include specific location for local buyers</Text>
        <Text style={styles.tipText}>📸 Add photos to attract more buyers (coming soon)</Text>
      </Card>

      <View style={styles.buttonContainer}>
        <Button
          title={loading ? 'Listing...' : 'List Crop for Sale'}
          onPress={handleSubmit}
          disabled={loading}
          style={styles.submitButton}
        />
        
        <Button
          title="Cancel"
          onPress={() => navigation.navigate('Home')}
          style={styles.cancelButton}
          textStyle={styles.cancelButtonText}
        />
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  buttonContainer: {
    marginTop: 20,
  },
  submitButton: {
    marginBottom: 10,
  },
  cancelButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#F44336',
  },
  cancelButtonText: {
    color: '#F44336',
  },
  tipText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    paddingLeft: 10,
  },
});

export default SellCropScreen;
