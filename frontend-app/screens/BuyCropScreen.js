import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, ScrollView, Alert, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import Card from '../components/Card';
import Button from '../components/Button';
import { buyCrops } from '../services/api';

const BuyCropScreen = () => {
  const [crops, setCrops] = useState([]);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const navigation = useNavigation();

  useEffect(() => {
    loadCrops();
  }, []);

  const loadCrops = async () => {
    setLoading(true);
    try {
      const response = await buyCrops();
      setCrops(response.items || []);
    } catch (error) {
      Alert.alert('Error', error.detail || 'Failed to load crops');
      // Mock data for demo
      setCrops([
        {
          id: '1',
          crop_name: 'Tomatoes',
          quantity_kg: 50,
          price_per_kg: 25,
          location: 'Bengaluru',
          notes: 'Fresh organic tomatoes',
          created_at: new Date().toISOString(),
        },
        {
          id: '2',
          crop_name: 'Potatoes',
          quantity_kg: 100,
          price_per_kg: 20,
          location: 'Mumbai',
          notes: 'Premium quality potatoes',
          created_at: new Date().toISOString(),
        },
        {
          id: '3',
          crop_name: 'Wheat',
          quantity_kg: 200,
          price_per_kg: 30,
          location: 'Delhi',
          notes: 'Organic wheat, pesticide-free',
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    loadCrops();
  };

  const handleContactSeller = (crop) => {
    Alert.alert(
      'Contact Seller',
      `Would you like to contact the seller for ${crop.crop_name}?`,
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Call', onPress: () => Alert.alert('Calling', `Calling seller for ${crop.crop_name}...`) },
        { text: 'Message', onPress: () => Alert.alert('Message', `Opening chat with seller...`) },
      ]
    );
  };

  const renderCropItem = ({ item }) => (
    <Card style={styles.cropCard}>
      <View style={styles.cropHeader}>
        <Text style={styles.cropName}>{item.crop_name}</Text>
        <View style={styles.priceBadge}>
          <Text style={styles.priceText}>₹{item.price_per_kg}/kg</Text>
        </View>
      </View>
      
      <View style={styles.cropDetails}>
        <View style={styles.detailRow}>
          <Text style={styles.detailLabel}>Quantity:</Text>
          <Text style={styles.detailValue}>{item.quantity_kg} kg</Text>
        </View>
        
        <View style={styles.detailRow}>
          <Text style={styles.detailLabel}>Location:</Text>
          <Text style={styles.detailValue}>{item.location}</Text>
        </View>
        
        <View style={styles.detailRow}>
          <Text style={styles.detailLabel}>Total Value:</Text>
          <Text style={styles.detailValue}>₹{(item.quantity_kg * item.price_per_kg).toFixed(2)}</Text>
        </View>
      </View>
      
      {item.notes && (
        <Text style={styles.notes}>{item.notes}</Text>
      )}
      
      <View style={styles.actionButtons}>
        <Button
          title="Contact Seller"
          onPress={() => handleContactSeller(item)}
          style={styles.contactButton}
        />
        <Button
          title="View Details"
          onPress={() => Alert.alert('Crop Details', `Full details for ${item.crop_name}`)}
          style={styles.detailsButton}
        />
      </View>
    </Card>
  );

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Available Crops</Text>
        <Text style={styles.subtitle}>Find fresh produce from local farmers</Text>
      </View>

      <View style={styles.filterContainer}>
        <TouchableOpacity style={styles.filterButton}>
          <Text style={styles.filterText}>All Crops</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.filterButton}>
          <Text style={styles.filterText}>Near Me</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.filterButton}>
          <Text style={styles.filterText}>Price</Text>
        </TouchableOpacity>
      </View>

      {loading && !refreshing ? (
        <View style={styles.loadingContainer}>
          <Text>Loading available crops...</Text>
        </View>
      ) : (
        <FlatList
          data={crops}
          renderItem={renderCropItem}
          keyExtractor={(item) => item.id}
          refreshing={refreshing}
          onRefresh={handleRefresh}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyText}>No crops available at the moment</Text>
              <Button
                title="Refresh"
                onPress={loadCrops}
                style={styles.refreshButton}
              />
            </View>
          }
          scrollEnabled={false}
        />
      )}

      <View style={styles.footer}>
        <Text style={styles.footerText}>
          {crops.length} crops available
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 20,
    backgroundColor: '#4CAF50',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: 'white',
    opacity: 0.9,
  },
  filterContainer: {
    flexDirection: 'row',
    padding: 15,
    backgroundColor: 'white',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  filterButton: {
    backgroundColor: '#f0f0f0',
    paddingVertical: 8,
    paddingHorizontal: 15,
    borderRadius: 20,
    marginRight: 10,
  },
  filterText: {
    fontSize: 14,
    color: '#666',
  },
  cropCard: {
    margin: 15,
    marginBottom: 5,
  },
  cropHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  cropName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  priceBadge: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 15,
  },
  priceText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 14,
  },
  cropDetails: {
    marginBottom: 10,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 5,
  },
  detailLabel: {
    fontSize: 14,
    color: '#666',
  },
  detailValue: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
  },
  notes: {
    fontSize: 14,
    color: '#666',
    fontStyle: 'italic',
    marginBottom: 15,
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  contactButton: {
    flex: 1,
    marginRight: 5,
    backgroundColor: '#2196F3',
  },
  detailsButton: {
    flex: 1,
    marginLeft: 5,
    backgroundColor: '#FF9800',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 50,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 50,
  },
  emptyText: {
    fontSize: 16,
    color: '#666',
    marginBottom: 20,
  },
  refreshButton: {
    backgroundColor: '#4CAF50',
  },
  footer: {
    padding: 15,
    alignItems: 'center',
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  footerText: {
    fontSize: 14,
    color: '#666',
  },
});

export default BuyCropScreen;
