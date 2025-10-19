import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_supabase_database():
    """Initialize Supabase database with required tables"""
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in .env file")
        return False
    
    print("🔄 Connecting to Supabase database...")
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url, sslmode='require')
        cursor = conn.cursor()
        
        print("✅ Connected to Supabase successfully!")
        
        # Create notes table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS note (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create index for better search performance
        CREATE INDEX IF NOT EXISTS idx_note_title ON note(title);
        CREATE INDEX IF NOT EXISTS idx_note_created_at ON note(created_at);
        
        -- Create a trigger to update updated_at automatically
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        
        DROP TRIGGER IF EXISTS update_note_updated_at ON note;
        CREATE TRIGGER update_note_updated_at
            BEFORE UPDATE ON note
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        
        print("✅ Database tables created successfully!")
        
        # Test insert
        cursor.execute("""
            INSERT INTO note (title, content) 
            VALUES ('Welcome Note', 'Welcome to your new note-taking app with Supabase!') 
            ON CONFLICT DO NOTHING
        """)
        conn.commit()
        
        # Check if data exists
        cursor.execute("SELECT COUNT(*) FROM note")
        count = cursor.fetchone()[0]
        
        print(f"✅ Database initialization complete! Found {count} notes in database.")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Initializing Supabase Database...")
    success = init_supabase_database()
    
    if success:
        print("\n🎉 Supabase setup complete! You can now run your app.")
        print("Next steps:")
        print("1. Run: python test_supabase.py (to test connection)")
        print("2. Run: python run_dev.py (to start your app)")
    else:
        print("\n❌ Setup failed. Please check your DATABASE_URL in .env file")