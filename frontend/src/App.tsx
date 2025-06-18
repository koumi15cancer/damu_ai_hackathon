import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Container,
  Paper,
  List,
  ListItem,
  ListItemText,
  Chip,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import axios from 'axios';

interface TeamMember {
  name: string;
  email: string;
  address: string;
  calendar_id?: string;
}

interface Suggestion {
  name: string;
  cost: string;
  duration: string;
  description: string;
  nearby_places?: Array<{
    name: string;
    address: string;
    rating?: number;
  }>;
}

interface TimeSlot {
  start: string;
  end: string;
}

function App() {
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [interests, setInterests] = useState<string[]>([]);
  const [budget, setBudget] = useState<string>('');
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [freeSlots, setFreeSlots] = useState<TimeSlot[]>([]);
  const [centralLocation, setCentralLocation] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [authDialogOpen, setAuthDialogOpen] = useState<boolean>(false);
  const [authUrl, setAuthUrl] = useState<string>('');

  const handleAddMember = () => {
    setTeamMembers([...teamMembers, { name: '', email: '', address: '' }]);
  };

  const handleMemberChange = (index: number, field: keyof TeamMember, value: string) => {
    const newMembers = [...teamMembers];
    newMembers[index] = { ...newMembers[index], [field]: value };
    setTeamMembers(newMembers);
  };

  const handleInterestChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInterests(event.target.value.split(',').map(i => i.trim()));
  };

  const handleGetAuthUrl = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/auth/url');
      setAuthUrl(response.data.auth_url);
      setAuthDialogOpen(true);
    } catch (error) {
      setError('Failed to get authentication URL');
    }
  };

  const handleAuthCallback = async (code: string) => {
    try {
      await axios.post('http://localhost:5000/api/auth/callback', { code });
      setAuthDialogOpen(false);
    } catch (error) {
      setError('Failed to authenticate with Google Calendar');
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5000/api/suggestions', {
        team_members: teamMembers,
        interests,
        budget: parseFloat(budget),
      });

      setSuggestions(response.data.suggestions);
      setFreeSlots(response.data.free_slots);
      setCentralLocation(response.data.central_location?.formatted_address || '');
    } catch (error) {
      setError('Failed to get suggestions');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Team Bonding Activity Suggester
        </Typography>

        <Paper sx={{ p: 3, mb: 3 }}>
          <form onSubmit={handleSubmit}>
            <Typography variant="h6" gutterBottom>
              Team Members
            </Typography>
            {teamMembers.map((member, index) => (
              <Box key={index} sx={{ mb: 2 }}>
                <TextField
                  fullWidth
                  label="Name"
                  value={member.name}
                  onChange={(e) => handleMemberChange(index, 'name', e.target.value)}
                  sx={{ mb: 1 }}
                />
                <TextField
                  fullWidth
                  label="Email"
                  value={member.email}
                  onChange={(e) => handleMemberChange(index, 'email', e.target.value)}
                  sx={{ mb: 1 }}
                />
                <TextField
                  fullWidth
                  label="Address"
                  value={member.address}
                  onChange={(e) => handleMemberChange(index, 'address', e.target.value)}
                />
              </Box>
            ))}
            <Button onClick={handleAddMember} sx={{ mb: 3 }}>
              Add Team Member
            </Button>

            <Typography variant="h6" gutterBottom>
              Preferences
            </Typography>
            <TextField
              fullWidth
              label="Interests (comma-separated)"
              value={interests.join(', ')}
              onChange={handleInterestChange}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Budget per person"
              type="number"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              sx={{ mb: 3 }}
            />

            <Button
              variant="contained"
              color="primary"
              type="submit"
              disabled={loading}
              sx={{ mr: 2 }}
            >
              {loading ? <CircularProgress size={24} /> : 'Get Suggestions'}
            </Button>
            <Button
              variant="outlined"
              onClick={handleGetAuthUrl}
              disabled={loading}
            >
              Connect Google Calendar
            </Button>
          </form>
        </Paper>

        {error && (
          <Typography color="error" sx={{ mb: 2 }}>
            {error}
          </Typography>
        )}

        {centralLocation && (
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Central Location
            </Typography>
            <Typography>{centralLocation}</Typography>
          </Paper>
        )}

        {freeSlots.length > 0 && (
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Available Time Slots
            </Typography>
            <List>
              {freeSlots.map((slot, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={`${new Date(slot.start).toLocaleString()} - ${new Date(slot.end).toLocaleString()}`}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        )}

        {suggestions.length > 0 && (
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Suggested Activities
            </Typography>
            <List>
              {suggestions.map((suggestion, index) => (
                <ListItem key={index} divider>
                  <ListItemText
                    primary={suggestion.name}
                    secondary={
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          Cost: {suggestion.cost}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Duration: {suggestion.duration}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {suggestion.description}
                        </Typography>
                        {suggestion.nearby_places && (
                          <Box sx={{ mt: 1 }}>
                            <Typography variant="subtitle2">Nearby Places:</Typography>
                            {suggestion.nearby_places.map((place, placeIndex) => (
                              <Chip
                                key={placeIndex}
                                label={`${place.name} (${place.rating || 'N/A'} ⭐)`}
                                size="small"
                                sx={{ mr: 1, mb: 1 }}
                              />
                            ))}
                          </Box>
                        )}
                      </Box>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        )}
      </Box>

      <Dialog open={authDialogOpen} onClose={() => setAuthDialogOpen(false)}>
        <DialogTitle>Google Calendar Authentication</DialogTitle>
        <DialogContent>
          <Typography>
            Please click the link below to authorize access to your Google Calendar:
          </Typography>
          <Button
            href={authUrl}
            target="_blank"
            rel="noopener noreferrer"
            fullWidth
            sx={{ mt: 2 }}
          >
            Authorize Google Calendar
          </Button>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAuthDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default App;
