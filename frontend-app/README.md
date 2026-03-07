# Smart Agriculture AI - React Native Mobile App

A complete mobile application for crop disease detection and agricultural marketplace.

## Features

- 🔍 **Crop Disease Scanning**: AI-powered disease detection using camera
- 🌾 **Marketplace**: Buy and sell crops with local farmers
- 👤 **User Authentication**: Secure login and registration
- 📱 **Modern UI**: Clean, intuitive interface designed for farmers

## Project Structure

```
frontend-app/
├── App.js                     # Main app entry point
├── navigation/
│   └── AppNavigator.js        # Navigation setup
├── screens/
│   ├── LoginScreen.js         # User login
│   ├── RegisterScreen.js      # User registration
│   ├── HomeScreen.js          # Main dashboard
│   ├── ScanScreen.js          # Camera scanning
│   ├── ResultScreen.js        # Disease results
│   ├── SellCropScreen.js      # Sell crops
│   └── BuyCropScreen.js       # Browse marketplace
├── components/
│   ├── Button.js              # Reusable button
│   ├── Input.js               # Reusable input field
│   └── Card.js                # Reusable card component
├── services/
│   └── api.js                 # API service layer
└── package.json               # Dependencies
```

## Technology Stack

- **React Native** with Expo
- **React Navigation** for routing
- **Axios** for API calls
- **Expo Camera** for image capture
- **Vector Icons** for icons

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- Expo CLI
- React Native development environment

### Installation

1. **Install dependencies:**
```bash
cd frontend-app
npm install
```

2. **Start the development server:**
```bash
npm start
```

3. **Run on device/emulator:**
```bash
# For Android
npm run android

# For iOS
npm run ios

# For Web
npm run web
```

### Backend Configuration

The app connects to your backend server at `http://localhost:8000`. Make sure:

1. **AI Model Server** is running on port 8001
2. **Backend Server** is running on port 9001
3. Update the API base URL in `services/api.js` if needed

```javascript
const API_BASE_URL = 'http://localhost:8000'; // Update if different
```

## API Endpoints Used

### Authentication
- `POST /login` - User login
- `POST /register` - User registration

### AI Services
- `POST /predict` - Crop disease detection

### Marketplace
- `POST /sell-crop` - List crop for sale
- `GET /buy-crops` - Browse available crops

## App Features

### 1. User Authentication
- Secure login with email/password
- User registration with validation
- Demo mode for hackathon testing

### 2. Disease Scanning
- Camera integration for leaf capture
- Image analysis using AI model
- Detailed treatment recommendations

### 3. Marketplace
- List crops for sale with details
- Browse available crops from other farmers
- Contact seller functionality

### 4. Modern UI/UX
- Clean, farmer-friendly interface
- Intuitive navigation
- Responsive design for all screen sizes

## Testing the App

### 1. Authentication Test
- Use any email/password for registration
- Login with registered credentials

### 2. Disease Scanning Test
- Grant camera permissions
- Take a photo of a plant leaf
- View AI analysis and recommendations

### 3. Marketplace Test
- Create a crop listing
- Browse available crops
- Test contact seller functionality

## Hackathon Tips

### Quick Demo Setup
1. Use demo credentials: `test@example.com` / `test123`
2. Test with sample leaf images from the dataset
3. Mock marketplace data for offline demos

### Performance Optimization
- Image compression before upload
- Caching for marketplace data
- Offline mode support

## Troubleshooting

### Common Issues

1. **Camera Permission Denied**
   - Enable camera permissions in device settings
   - Reinstall the app if needed

2. **API Connection Error**
   - Verify backend servers are running
   - Check network connectivity
   - Update API base URL if needed

3. **Build Errors**
   - Clear Expo cache: `expo r -c`
   - Reinstall dependencies: `npm install`
   - Update Expo CLI: `npm install -g expo-cli`

## Future Enhancements

- 📍 GPS-based location services
- 💳 Payment integration
- 📊 Analytics dashboard
- 🔔 Push notifications
- 🌐 Multi-language support
- 📱 Offline mode support

## License

MIT License - feel free to use for hackathons and development.
