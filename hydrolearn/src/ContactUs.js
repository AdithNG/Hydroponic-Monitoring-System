import React from 'react';

const ContactUs = () => {
    return (
        <div style={styles.container}>
            <h1 style={styles.title}>Contact Us</h1>
            <p style={styles.text}>We would love to hear from you! If you have any questions or need assistance, feel free to reach out to us.</p>
            <div style={styles.contactContainer}>
                <div style={styles.contactCard}>
                    <h3 style={styles.name}>Adith Nishanth Gunaseelan</h3>
                    <p style={styles.role}>Software Engineer & Full-stack Developer</p>
                    <p>Email: <a href="mailto:adithnishanth@gmail.com">adithnishanth@gmail.com</a></p>
                    <p>Phone: <a href="tel:+16673454053">+1 (667) 345-4053</a></p>
                </div>
                <div style={styles.contactCard}>
                    <h3 style={styles.name}>Anjali Nilendu Jha</h3>
                    <p style={styles.role}>Database Engineer</p>
                    <p>Phone: <a href="tel:+917276674119">+91 72766 74119</a></p>
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
    contactContainer: {
        display: 'flex',
        justifyContent: 'space-around',
        flexWrap: 'wrap',
    },
    contactCard: {
        backgroundColor: '#ffffff',
        padding: '20px',
        borderRadius: '10px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        marginBottom: '20px',
        maxWidth: '300px',
        textAlign: 'left',
    },
    name: {
        fontSize: '1.5em',
        marginBottom: '10px',
        color: '#333',
    },
    role: {
        fontSize: '1.2em',
        marginBottom: '10px',
        fontStyle: 'italic',
        color: '#666',
    },
};

export default ContactUs;
