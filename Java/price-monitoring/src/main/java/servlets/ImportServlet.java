package servlets;

import entities.ProductEntity;
import repositories.product.ProductRepository;
import util.csv.CSVImport;

import javax.inject.Inject;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

//@WebServlet(name = "ImportServlet", urlPatterns = {"/import"})
public class ImportServlet extends HttpServlet {
    @Inject
    CSVImport csvImport;

    @Inject
    ProductRepository repository;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String source = request.getParameter("source");
        csvImport.startImport(source);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

    }
}
