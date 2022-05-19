#include "GRPCService.hpp"

#include <exception>
#include <iostream>

// ============================================================================
// GRPCService PUBLIC METHODS
// ============================================================================

// GRPCService Ctor. & Dtor.
// ----------------------------------------------------------------------------

ansys::grpc::service::GRPCService::GRPCService() {
    // Start creating the GRPCService object
    std::cout << "GRPCService object created." << std::endl;
}

ansys::grpc::service::GRPCService::~GRPCService() {
    // Start destroying the GRPCService object
    std::cout << "GRPCService object destroyed." << std::endl;
}

// GRPCService Functionalities
// ----------------------------------------------------------------------------

::grpc::Status ansys::grpc::service::GRPCService::SayHello(
    ::grpc::ServerContext* context, const ::grpcdemo::HelloRequest* request,
    ::grpcdemo::HelloReply* response) {
    // Log event
    std::cout << ">>>> Greeting requested! Requested by " << request->name()
              << std::endl;

    // Define the response!
    response->set_message("Hello, " + request->name() + "!");
    return ::grpc::Status::OK;
}

::grpc::Status ansys::grpc::service::GRPCService::FlipVector(
    ::grpc::ServerContext* context, const ::grpcdemo::Vector* request,
    ::grpcdemo::Vector* response) {
    // Log event
    std::cout << ">>>> Vector flip requested!" << std::endl;

    // First, deserialize our vector into an Eigen::VectorXd object
    auto vec = deserialize_vector(request->vector_as_chunk(),
                                  request->vector_size(), request->data_type());
    std::cout << ">>>> Incoming Vector: " << vec.transpose() << std::endl;

    // Flip the vector
    Eigen::VectorXd flip_vec = vec.reverse();

    // Log the result
    std::cout << ">>>> Result of vector flip: " << flip_vec.transpose()
              << std::endl;

    // Send the response
    response->set_data_type(request->data_type());
    response->set_vector_size(request->vector_size());
    response->set_vector_as_chunk(serialize_vector(flip_vec));
    return ::grpc::Status::OK;
}

::grpc::Status ansys::grpc::service::GRPCService::AddVectors(
    ::grpc::ServerContext* context,
    ::grpc::ServerReader< ::grpcdemo::Vector>* reader,
    ::grpcdemo::Vector* response) {
    // Log event
    std::cout << ">>>> Vector addition requested!" << std::endl;

    // Initialize our result variable
    Eigen::VectorXd result{};

    // First, deserialize our vectors into Eigen::VectorXd objects
    grpcdemo::Vector message;

    // Use the reader to process all messages individually
    while (reader->Read(&message)) {
        auto vec =
            deserialize_vector(message.vector_as_chunk(), message.vector_size(),
                               message.data_type());
        std::cout << ">>>> Incoming Vector: " << vec.transpose() << std::endl;

        // Perform some checks
        if (result.size() == 0) {
            // This means that our vector has not been initialized yet!
            result = vec;
        } else if (vec.size() != result.size()) {
            // This means that the incoming vectors have different sizes... This
            // is not supported!
            std::string error{
                ">>>> ERR: Incoming vectors are of different sizes."};
            std::cout << error << std::endl;
            return ::grpc::Status(::grpc::StatusCode::CANCELLED, error);
        } else {
            // Otherwise, everything is OK... Perform the addition!
            result += vec;
        }
    }

    // Log the result
    std::cout << ">>>> Result of addition: " << result.transpose() << std::endl;

    // Send the response
    response->set_data_type(grpcdemo::DataType::DOUBLE);
    response->set_vector_size(result.size());
    response->set_vector_as_chunk(serialize_vector(result));
    return ::grpc::Status::OK;
}

::grpc::Status ansys::grpc::service::GRPCService::MultiplyVectors(
    ::grpc::ServerContext* context,
    ::grpc::ServerReader< ::grpcdemo::Vector>* reader,
    ::grpcdemo::Vector* response) {
    // Log event
    std::cout << ">>>> Vector dot product requested!" << std::endl;

    // First, deserialize our vectors into Eigen::VectorXd objects
    grpcdemo::Vector message;

    // Use the reader to process all messages individually - Since it cannot be
    // an infinite number of vectors, we will call the method twice manually
    Eigen::VectorXd vec1{}, vec2{};
    if (reader->Read(&message)) {
        vec1 = deserialize_vector(message.vector_as_chunk(),
                                  message.vector_size(), message.data_type());
        std::cout << ">>>> Incoming Vector: " << vec1.transpose() << std::endl;
    } else {
        // This means that there are no incoming vectors... This is not
        // supported!
        std::string error{">>>> ERR: No incoming vector 1."};
        std::cout << error << std::endl;
        return ::grpc::Status(::grpc::StatusCode::CANCELLED, error);
    }

    if (reader->Read(&message)) {
        vec2 = deserialize_vector(message.vector_as_chunk(),
                                  message.vector_size(), message.data_type());
        std::cout << ">>>> Incoming Vector: " << vec2.transpose() << std::endl;
    } else {
        // This means that there are no sufficient incoming vectors... This is
        // not supported!
        std::string error{">>>> ERR: No incoming vector 2."};
        std::cout << error << std::endl;
        return ::grpc::Status(::grpc::StatusCode::CANCELLED, error);
    }

    // Perform the dot product
    double dot_product;
    if (vec1.size() != vec2.size()) {
        // This means that the incoming vectors have different sizes... This
        // is not supported!
        std::string error{">>>> ERR: Incoming vectors are of different sizes."};
        std::cout << error << std::endl;
        return ::grpc::Status(::grpc::StatusCode::CANCELLED, error);
    } else {
        dot_product = vec1.dot(vec2);
    }

    // Build the result Eigen::VectorXd
    Eigen::VectorXd result{};
    result.resize(1);
    result << dot_product;

    // Log the result
    std::cout << ">>>> Result of dot product: " << std::endl;
    std::cout << result << std::endl;

    // Send the response
    response->set_data_type(grpcdemo::DataType::DOUBLE);
    response->set_vector_size(result.size());
    response->set_vector_as_chunk(serialize_vector(result));
    return ::grpc::Status::OK;
}

::grpc::Status ansys::grpc::service::GRPCService::AddMatrices(
    ::grpc::ServerContext* context,
    ::grpc::ServerReader< ::grpcdemo::Matrix>* reader,
    ::grpcdemo::Matrix* response) {
    // Log event
    std::cout << ">>>> Matrix addition requested!" << std::endl;

    // Initialize our result variable
    Eigen::MatrixXd result{};

    // First, deserialize our matrices into Eigen::MatrixXd objects
    grpcdemo::Matrix message;

    // Use the reader to process all messages individually
    while (reader->Read(&message)) {
        auto mat =
            deserialize_matrix(message.matrix_as_chunk(), message.matrix_rows(),
                               message.matrix_cols(), message.data_type());
        std::cout << ">>>> Incoming Matrix: " << std::endl;
        std::cout << mat << std::endl;

        // Perform some checks
        if (result.size() == 0) {
            // This means that our matrix has not been initialized yet!
            result = mat;
        } else if (mat.rows() != result.rows() || mat.cols() != result.cols()) {
            // This means that the incoming matrices have different sizes...
            // This is not supported!
            std::string error{
                ">>>> ERR: Incoming matrices are of different sizes."};
            std::cout << error << std::endl;
            return ::grpc::Status(::grpc::StatusCode::CANCELLED, error);
        } else {
            // Otherwise, everything is OK... Perform the addition!
            result += mat;
        }
    }

    // Log the result
    std::cout << ">>>> Resulting Matrix: " << std::endl;
    std::cout << result << std::endl;

    // Send the response
    response->set_data_type(grpcdemo::DataType::DOUBLE);
    response->set_matrix_rows(result.rows());
    response->set_matrix_cols(result.cols());
    response->set_matrix_as_chunk(serialize_matrix(result));
    return ::grpc::Status::OK;
}

::grpc::Status ansys::grpc::service::GRPCService::MultiplyMatrices(
    ::grpc::ServerContext* context,
    ::grpc::ServerReader< ::grpcdemo::Matrix>* reader,
    ::grpcdemo::Matrix* response) {
    // Log event
    std::cout << ">>>> Matrix multiplication requested!" << std::endl;

    // Initialize our result variable
    Eigen::MatrixXd result{};

    // First, deserialize our matrices into Eigen::MatrixXd objects
    grpcdemo::Matrix message;

    // Use the reader to process all messages individually
    while (reader->Read(&message)) {
        auto mat =
            deserialize_matrix(message.matrix_as_chunk(), message.matrix_rows(),
                               message.matrix_cols(), message.data_type());
        std::cout << ">>>> Incoming Matrix: " << std::endl;
        std::cout << mat << std::endl;

        // Perform some checks
        if (result.size() == 0) {
            // This means that our matrix has not been initialized yet!
            result = mat;
        } else if (mat.rows() != result.cols() || mat.cols() != result.rows()) {
            // This means that the incoming matrices have incompatible sizes...
            // This is not supported!
            std::string error{
                ">>>> ERR: Incoming matrices are of different sizes."};
            std::cout << error << std::endl;
            return ::grpc::Status(::grpc::StatusCode::CANCELLED, error);
        } else {
            // Otherwise, everything is OK... Perform the multiplication!
            result *= mat;
        }
    }

    // Log the result
    std::cout << ">>>> Resulting Matrix: " << std::endl;
    std::cout << result << std::endl;

    // Send the response
    response->set_data_type(grpcdemo::DataType::DOUBLE);
    response->set_matrix_rows(result.rows());
    response->set_matrix_cols(result.cols());
    response->set_matrix_as_chunk(serialize_matrix(result));
    return ::grpc::Status::OK;
}

// ============================================================================
// GRPCService PRIVATE METHODS
// ============================================================================

Eigen::VectorXd ansys::grpc::service::GRPCService::deserialize_vector(
    const std::string& bytes, const int length, grpcdemo::DataType type) {
    // Get the step of the bytes array to interpret each type
    int step{0};
    switch (type) {
        case grpcdemo::DataType::DOUBLE:
            step = sizeof(double);
            break;
        case grpcdemo::DataType::INTEGER:
            step = sizeof(int);
            break;
        default:
            throw std::invalid_argument("Invalid Vector type!");
    }

    // Interpret the stream of bytes
    Eigen::VectorXd vector{};
    vector.resize(length);

    // Turn into a const char*
    auto ptr = bytes.data();

    // Loop over the stream of bytes
    for (int idx = 0; idx < length; idx++) {
        memcpy(&vector[idx], ptr, step);
        ptr += step;
    }

    // Return the vector
    return vector;
}

std::string ansys::grpc::service::GRPCService::serialize_vector(
    const Eigen::VectorXd& vector) {
    // Initialize the serialized vector
    std::string vec_as_str{};

    // Loop over all vector elements
    for (int idx = 0; idx < vector.size(); ++idx) {
        // We will assume that all elements are of type double
        const unsigned char* ptr =
            reinterpret_cast<const unsigned char*>(&vector[idx]);

        // Serialize!
        for (size_t i = 0; i < sizeof(double); ++i)
            vec_as_str.push_back(ptr[i]);
    }

    // Return the vector "serialized"
    return vec_as_str;
}

Eigen::MatrixXd ansys::grpc::service::GRPCService::deserialize_matrix(
    const std::string& bytes, const int rows, const int cols,
    grpcdemo::DataType type) {
    // Get the step of the bytes array to interpret each type
    int step{0};
    switch (type) {
        case grpcdemo::DataType::DOUBLE:
            step = sizeof(double);
            break;
        case grpcdemo::DataType::INTEGER:
            step = sizeof(int);
            break;
        default:
            throw std::invalid_argument("Invalid Matrix type!");
    }

    // Interpret the stream of bytes
    Eigen::MatrixXd matrix{};
    matrix.resize(rows, cols);

    // Turn into a const char*
    auto ptr = bytes.data();

    // Loop over the stream of bytes
    for (int row_idx = 0; row_idx < rows; row_idx++) {
        for (int col_idx = 0; col_idx < cols; col_idx++) {
            memcpy(&matrix(row_idx, col_idx), ptr, step);
            ptr += step;
        }
    }

    // Return the matrix
    return matrix;
}

std::string ansys::grpc::service::GRPCService::serialize_matrix(
    const Eigen::MatrixXd& matrix) {
    // Initialize the serialized matrix
    std::string mat_as_str{};

    // Loop over all elements in the matrix: rows --> highest level
    for (int row_idx = 0; row_idx < matrix.rows(); ++row_idx) {
        for (int col_idx = 0; col_idx < matrix.cols(); ++col_idx) {
            // We will assume that all elements are of type double
            const unsigned char* ptr = reinterpret_cast<const unsigned char*>(
                &matrix(row_idx, col_idx));

            // Serialize!
            for (size_t i = 0; i < sizeof(double); ++i)
                mat_as_str.push_back(ptr[i]);
        }
    }

    // Return the matrix "serialized"
    return mat_as_str;
}

// ============================================================================
// ansys::grpc::server NAMESPACE METHODS
// ============================================================================