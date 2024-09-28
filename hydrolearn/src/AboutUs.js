import React from 'react';

const AboutUs = () => {
    return (
        <div style={styles.container}>
            <h1 style={styles.title}>About HydroLearn</h1>
            <p style={styles.text}>
                HydroLearn was created by a passionate team dedicated to making hydroponic farming more efficient and accessible. 
                Our mission is to provide growers with real-time monitoring and insights to ensure optimal growing conditions 
                for their plants. Through our platform, you can easily track and manage key parameters like temperature, humidity, and pH levels.
            </p>
            <p style={styles.text}>
                Our team consists of experts from various fields, including data analytics, software engineering, and agriculture technology. 
                Our vision is to empower hydroponic enthusiasts and professionals alike with the tools needed to grow smarter and 
                healthier plants, while maximizing yield and minimizing resource usage.
            </p>
            <h2 style={styles.subtitle}>Meet the Team</h2>
            <div style={styles.teamContainer}>
                <div style={styles.teamMember}>
                    <h3 style={styles.memberName}>Adith Nishanth Gunaseelan</h3>
                    <img src="/Adith.jpg" alt="Adith Nishanth Gunaseelan" style={styles.teamImage} />
                    <p style={styles.memberRole}>Software Engineer & Full-stack Developer</p>
                    <p style={styles.memberBio}>Adith specializes in building robust systems and ensuring the smooth integration of real-time data pipelines with user-facing web applications.</p>
                </div>
                <div style={styles.teamMember}>
                    <h3 style={styles.memberName}>Anjali</h3>
                    <p style={styles.memberRole}>Database Engineer</p>
                    <p style={styles.memberBio}>Anjali manages and optimizes the MongoDB database, ensuring that HydroLearn operates smoothly with real-time data access and storage capabilities.</p>
                </div>
            </div>
        </div>
    );
};

const styles = {
    container: {
        padding: '50px',
        maxWidth: '800px',
        margin: '0 auto',
        textAlign: 'center',
        backgroundColor: '#f5f5f5',
        borderRadius: '10px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    },
    title: {
        fontSize: '3em',
        marginBottom: '20px',
        color: '#333',
    },
    text: {
        fontSize: '1.2em',
        marginBottom: '20px',
        color: '#555',
    },
    subtitle: {
        fontSize: '2em',
        marginTop: '40px',
        marginBottom: '20px',
        color: '#333',
    },
    teamContainer: {
        display: 'flex',
        justifyContent: 'space-around',
        flexWrap: 'wrap',
    },
    teamMember: {
        backgroundColor: '#ffffff',
        padding: '20px',
        borderRadius: '10px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        marginBottom: '20px',
        maxWidth: '300px',
        textAlign: 'left',
    },
    teamImage: {
        width: '100%',
        borderRadius: '10px',
        marginBottom: '15px',
    },
    memberName: {
        fontSize: '1.5em',
        marginBottom: '10px',
        color: '#333',
    },
    memberRole: {
        fontSize: '1.2em',
        marginBottom: '10px',
        fontStyle: 'italic',
        color: '#666',
    },
    memberBio: {
        fontSize: '1em',
        color: '#555',
    },
};

export default AboutUs;
