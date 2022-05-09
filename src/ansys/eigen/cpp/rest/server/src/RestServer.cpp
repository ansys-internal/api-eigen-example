#include "RestServer.hpp"

#include <stdio.h>

#include "EigenFunctionalities.hpp"
#include "RestDb.hpp"

ansys::rest::RestServer::RestServer() {
    CROW_LOG_INFO << "REST Server object instantiated.";

    // We are defining how we want this endpoint to behave
    //
    // GREETING ENDPOINT
    //==================
    CROW_ROUTE(_app, "/")
    ([](const crow::request& req) {
        return "Greetings from the REST Eigen Server (implemented in C++)!";
    });

    // VECTORS ENDPOINT - RESOURCE
    //============================
    vector_resource_endpoints();

    // MATRICES ENDPOINT - RESOURCE
    //=============================
    matrix_resource_endpoints();

    // VECTORS OPS. - RESOURCE
    //========================
    vector_operations_endpoints();

    // MATRICES OPS. - RESOURCE
    //=========================
    matrix_operations_endpoints();
}

ansys::rest::RestServer::~RestServer() {
    CROW_LOG_INFO << "REST Server object destroyed.";
}

void ansys::rest::RestServer::serve(const int port, const bool async,
                                    const crow::LogLevel logLevel) {
    // Set the servers logging level we have decided
    _app.loglevel(logLevel);

    // Now, serve depending on whether we want it to run asynchronously or not
    // We define the app, with its port, and in multi-thread config... and set
    // it to run accordingly!
    if (async) {
        _app.port(port).multithreaded().run();
    } else {
        _app.port(port).multithreaded().run_async();
    }
}

void ansys::rest::RestServer::vector_resource_endpoints() {
    // Define how the different "Vectors" resource endpoints should behave
    //
    // 1) ENDPOINT for POSTING VECTORS
    // ===============================
    CROW_ROUTE(_app, "/Vectors")
        .methods(crow::HTTPMethod::POST)([&](const crow::request& req) {
            // Check if the provided input can be processed
            EigenFunctionalities::read_vector(req.body);

            // Inform the user that the processing was successful
            CROW_LOG_INFO << "Entry succesfully processed: " + req.body;
            CROW_LOG_INFO << "Attempting to store in DB...";

            // Store into the DB and retrieve its ID
            long id =
                _db.store_resource(ansys::rest::db::DbTypes::VECTOR, req.body);

            // Define the response code and message
            CROW_LOG_INFO << "Storage in DB succesfull. Creating response.";
            auto responseBody = crow::json::wvalue(
                {{"vector", crow::json::wvalue({{"id", id}})}});

            // Send the response
            return crow::response(201, responseBody);
        });

    // 2) ENDPOINT for GETTING VECTORS
    // ===============================
    CROW_ROUTE(_app, "/Vectors(<int>)")
        .methods(crow::HTTPMethod::GET)([&](int id) {
            CROW_LOG_INFO << "Attempting to load resource from DB...";

            // Load from the DB given its ID
            auto resource =
                _db.load_resource(ansys::rest::db::DbTypes::VECTOR, id);

            if (resource.empty()) {
                // Define the response code and message
                CROW_LOG_INFO << "Entry not found. Creating response.";

                // Send the response
                return crow::response(404, "Entry not found");
            } else {
                // Define the response code and message
                CROW_LOG_INFO << "Search in DB succesfull. Creating response.";

                // Send the response
                return crow::response(200, resource);
            }
        });
}

void ansys::rest::RestServer::matrix_resource_endpoints() {
    // Define how the different "Matrices" resource endpoints should behave
    //
    // 1) ENDPOINT for POSTING MATRICES
    // ================================
    CROW_ROUTE(_app, "/Matrices")
        .methods(crow::HTTPMethod::POST)([&](const crow::request& req) {
            // Check if the provided input can be processed
            EigenFunctionalities::read_matrix(req.body);

            // Inform the user that the processing was successful
            CROW_LOG_INFO << "Entry succesfully processed: " + req.body;
            CROW_LOG_INFO << "Attempting to store in DB...";

            // Store into the DB and retrieve its ID
            long id =
                _db.store_resource(ansys::rest::db::DbTypes::MATRIX, req.body);

            // Define the response code and message
            CROW_LOG_INFO << "Storage in DB succesfull. Creating response.";
            auto responseBody = crow::json::wvalue(
                {{"matrix", crow::json::wvalue({{"id", id}})}});

            // Send the response
            return crow::response(201, responseBody);
        });

    // 2) ENDPOINT for GETTING MATRICES
    // ================================
    CROW_ROUTE(_app, "/Matrices(<int>)")
        .methods(crow::HTTPMethod::GET)([&](int id) {
            CROW_LOG_INFO << "Attempting to load resource from DB...";

            // Load from the DB given its ID
            auto resource =
                _db.load_resource(ansys::rest::db::DbTypes::MATRIX, id);

            if (resource.empty()) {
                // Define the response code and message
                CROW_LOG_INFO << "Entry not found. Creating response.";

                // Send the response
                return crow::response(404, "Entry not found");
            } else {
                // Define the response code and message
                CROW_LOG_INFO << "Search in DB succesfull. Creating response.";

                // Send the response
                return crow::response(200, resource);
            }
        });
}

void ansys::rest::RestServer::vector_operations_endpoints() {}

void ansys::rest::RestServer::matrix_operations_endpoints() {}