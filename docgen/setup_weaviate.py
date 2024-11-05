import weaviate
from weaviate import WeaviateClient
import weaviate.classes as wvc
from weaviate.classes.config import Configure

def setup_weaviate():
    # Initialize the client with v4 syntax, including gRPC port
    client = WeaviateClient(
        connection_params=weaviate.connect.ConnectionParams.from_url(
            url="http://localhost:8080",
            grpc_port=50051
        )
    )

    # Connect to the client
    client.connect()

    # Define the schema with proper property definitions for v4
    properties = [
        wvc.config.Property(
            name="content",
            data_type=wvc.config.DataType.TEXT,
            description="The content of the document"
        ),
        wvc.config.Property(
            name="metadata",
            data_type=wvc.config.DataType.OBJECT,
            nested_properties=[
                wvc.config.Property(
                    name="source",
                    data_type=wvc.config.DataType.TEXT,
                    description="Source of the document"
                ),
                wvc.config.Property(
                    name="created_at",
                    data_type=wvc.config.DataType.DATE,
                    description="Creation timestamp"
                ),
                wvc.config.Property(
                    name="title",
                    data_type=wvc.config.DataType.TEXT,
                    description="Document title"
                ),
                wvc.config.Property(
                    name="description",
                    data_type=wvc.config.DataType.TEXT,
                    description="Document description"
                ),
                wvc.config.Property(
                    name="language",
                    data_type=wvc.config.DataType.TEXT,
                    description="Document language"
                ),
                wvc.config.Property(
                    name="url",
                    data_type=wvc.config.DataType.TEXT,
                    description="Document URL"
                ),
                wvc.config.Property(
                    name="og_title",
                    data_type=wvc.config.DataType.TEXT,
                    description="OpenGraph title"
                ),
                wvc.config.Property(
                    name="og_description",
                    data_type=wvc.config.DataType.TEXT,
                    description="OpenGraph description"
                ),
                wvc.config.Property(
                    name="og_image",
                    data_type=wvc.config.DataType.TEXT,
                    description="OpenGraph image URL"
                ),
                wvc.config.Property(
                    name="twitter_card",
                    data_type=wvc.config.DataType.TEXT,
                    description="Twitter card type"
                ),
                wvc.config.Property(
                    name="twitter_image",
                    data_type=wvc.config.DataType.TEXT,
                    description="Twitter image URL"
                )
            ]
        )
    ]

    try:
        # Delete existing collection if it exists
        try:
            client.collections.delete("Document")
        except Exception as e:
            print(f"No existing collection to delete: {e}")

        # Create the collection using v4 API
        client.collections.create(
            name="Document",
            properties=properties,
            vectorizer_config=Configure.Vectorizer.none()
        )
        print("Schema created successfully")
        
    except Exception as e:
        print(f"Error creating schema: {str(e)}")
        raise
    finally:
        client.close()

    return client

if __name__ == "__main__":
    setup_weaviate()