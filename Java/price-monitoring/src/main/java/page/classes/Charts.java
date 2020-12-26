package page.classes;

import entities.ProductEntity;
import entities.ProductHistoryEntity;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import org.primefaces.model.charts.ChartData;
import org.primefaces.model.charts.line.LineChartDataSet;
import org.primefaces.model.charts.line.LineChartModel;
import org.primefaces.model.charts.line.LineChartOptions;
import org.primefaces.model.charts.optionconfig.title.Title;

import javax.annotation.PostConstruct;
import javax.enterprise.context.RequestScoped;
import javax.faces.context.FacesContext;
import javax.inject.Named;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Named
@RequestScoped
@Getter
@Setter
public class Charts {
    private LineChartModel lineModel;

    @Getter(AccessLevel.PRIVATE)
    @Setter(AccessLevel.PRIVATE)
    private ProductEntity productEntity;

    @PostConstruct
    public void init(){
        Map<String, Object> parameterValue = FacesContext.getCurrentInstance().getExternalContext().getSessionMap();
        productEntity = (ProductEntity) parameterValue.get("product_for_evaluation");

        createLineModel();
    }

    public void createLineModel() {
        lineModel = new LineChartModel();
        ChartData data = new ChartData();

        LineChartDataSet dataSet = new LineChartDataSet();
        List<Number> values = new ArrayList<>();
        List<String> labels = new ArrayList<>();

        for(ProductHistoryEntity productHistoryEntity : productEntity.getHistory()){
            values.add(productHistoryEntity.getPrice());
            labels.add(productHistoryEntity.getDate().toString());
        }

//        values.add(65);
//        values.add(59);
//        values.add(80);
//        values.add(81);
//        values.add(56);
//        values.add(55);
//        values.add(40);
//
//        labels.add("January");
//        labels.add("February");
//        labels.add("March");
//        labels.add("April");
//        labels.add("May");
//        labels.add("June");
//        labels.add("July");

        dataSet.setData(values);
        dataSet.setFill(false);
        dataSet.setLabel("My First Dataset");
        dataSet.setBorderColor("rgb(75, 192, 192)");
        dataSet.setLineTension(0.1);
        data.addChartDataSet(dataSet);
        data.setLabels(labels);

        //Options
        LineChartOptions options = new LineChartOptions();
        Title title = new Title();
        title.setDisplay(true);
        title.setText("Line Chart");
        options.setTitle(title);

        lineModel.setOptions(options);
        lineModel.setData(data);
    }
}
